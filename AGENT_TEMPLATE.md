# AGENT_TEMPLATE.md - Constitutional Agent Skeleton

## Quick Start
Copy agents/lawclaw/agent_handler.py to agents/YOURAGENT/agent_handler.py
Then modify:
1. Replace all "lawclaw" with "youragent"
2. Replace all "LawClawHandler" with "YourAgentHandler"
3. Replace /help text with your agent's commands
4. Add your domain-specific elif blocks for each command
5. Create commands/_memory.py (copy from lawclaw, change agent name)
6. Create commands/_helpers.py (copy from lawclaw, adapt utilities)

## Constitutional Requirements
Every agent MUST have:
- call_agent() boundary for cross-agent delegation
- Capability routing (get_capable_agent in else clause)
- All LLM through Sovereign Gateway (shared/llm/client.py)
- All exceptions logged via log_err()
- /help and /stats must NOT call _gather_context() (latency)
- No constitutional boundary dead block (removed May 30)

## Handler Structure
- __init__: super().__init__("agentname")
- _gather_context(): use cached_search() for retrieval, returns context string
- handle(): if/elif chain for commands, else clause with capability routing
- Lifecycle cleanup handled by a2a_server.py, not individual handlers

## Retrieval: Use cached_search()

```python
def _gather_context(self, query=""):
    parts = []
    # Primary retrieval via cache + WebClaw BM25 pipeline
    web = self.cached_search(f"ns:{{self.name}} {query}")
    if web:
        parts.append(str(web)[:2000])
    # Supplementary: local data via DataClaw
    data = self.call_agent("dataclaw", f"/search ns:{{self.name}} {query}", timeout=15)
    if data:
        parts.append(str(data)[:2000])
    return "\n".join(parts)
```

cached_search() provides:
- DataClaw cache check (24hr TTL)
- WebClaw BM25 fallback (provider + chronicle + dedup + source confidence)
- Automatic cache write for future queries
- [CACHED] marker on cache hits

## API Methods Available (from BaseAgent)
- self.ask_llm(prompt) - Sovereign Gateway (Groq->Ollama->OpenRouter->Anthropic)
- self.call_agent(name, task, timeout) - cross-agent delegation with circuit breaker
- self.cached_search(query) - cache-first retrieval with WebClaw BM25 fallback
- self.search_chronicle(query, limit) - 448MB SQLite FTS5
- self.get_cached_result(agent, query) - retrieve from DataClaw cache
- self.cache_result(agent, query, results) - store to DataClaw cache
- log_err(agent, context, error) - from shared/_agent_helpers.py

## Command File Pattern
Each command in commands/ directory:
- name = "/commandname"
- def run(args, agent=None): returns string
- Use agent.cached_search() for retrieval (cache + BM25)
- Use agent.ask_llm() for LLM calls (never direct API)
- Pass agent=self from handler for context access

## Provider Chain (June 5, 2026)
| Priority | Provider | Model | Latency | Cost |
|----------|----------|-------|---------|------|
| 1 | Groq | llama-3.3-70b-versatile | 0.7s | Free tier |
| 2 | Ollama | gemma3:4b | 0.8s GPU | Free (local) |
| 3 | OpenRouter | google/gemma-4-26b-a4b-it:free | 0.7s | Free tier |
| 4 | Anthropic | claude-haiku-4-5-20251001 | 1.2s | Paid |

Switch: llmclaw> /use groq
GPU: GTX 970, 4GB VRAM. Fits: gemma3:4b (3.3GB). Does NOT fit: deepseek-r1:8b (5.2GB).

## Verification
```bash
python -c "import requests; r=requests.post('http://127.0.0.1:8766/v1/message/YOURAGENT',json={'task':'/help'},timeout=10); print(r.status_code, len(r.text))"
```
Should return 200 with non-empty response.

```bash
python scripts/validate_agents.py
```
Should show 21/21 agents pass.
