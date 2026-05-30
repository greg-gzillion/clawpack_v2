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
- Shared memory bridge (_memory.py with show_prior + remember)
- All LLM through Sovereign Gateway (shared/llm/client.py)
- All exceptions logged via log_err()
- /help and /stats must NOT call _gather_context() (6s latency bug)

## Handler Structure (what lawclaw/agent_handler.py contains)
- __init__: super().__init__("agentname")
- _gather_context(): calls webclaw + search_chronicle, returns context string
- handle(): if/elif chain for commands, else clause with capability routing
- else block: get_capable_agent -> call_agent or ask_llm fallback
- No 23-system boundary block (removed May 30 - caused 6s /help latency)
- Lifecycle cleanup handled by a2a_server.py, not individual handlers

## API Methods Available (from BaseAgent)
- self.ask_llm(prompt) - Sovereign Gateway (Groq->Ollama->OpenRouter->Anthropic)
- self.call_agent(name, task, timeout) - cross-agent delegation
- self.search_chronicle(query, limit) - 448MB SQLite FTS5
- self.lookup_jurisdiction(city, type) - 3,800+ cities (hospital/police/library/codes)
- self.search_web(query) - via webclaw, cached 24hr
- log_err(agent, context, error) - from shared/_agent_helpers.py

## Command File Pattern
Each command in commands/ directory:
- name = "/commandname" 
- def run(args, agent=None): returns string
- Use agent.lookup_jurisdiction() for civic data (0.03s via Chronicle FTS5)
- Use agent.ask_llm() for LLM calls (never direct API)
- Import show_prior/remember from _memory for cross-session recall

## Provider Chain (May 30, 2026)
| Priority | Provider | Model | Latency |
|----------|----------|-------|---------|
| 1 | Groq | llama-3.3-70b-versatile | 0.7s |
| 2 | Ollama | deepseek-r1:8b | 0.8s |
| 3 | OpenRouter | google/gemma-4-26b-a4b-it:free | 0.7s |
| 4 | Anthropic | claude-haiku-4-5-20251001 | 1.2s |

## Key Differences from Pre-May-30 Templates
- No 23-system boundary block (removed - caused 6s latency)
- No log_event import (removed from chronicle_ledger)
- No DecisionLedger.record(action=...) (signature changed to record_action)
- Commands pass agent=self for jurisdiction lookups
- Skip _gather_context() for /help and /stats

## Verification
python -c "import requests; r=requests.post('http://127.0.0.1:8766/v1/message/YOURAGENT',json={'task':'/help'},timeout=10); print(r.status_code, len(r.text))"
Should return 200 with non-empty response in under 0.5s.
