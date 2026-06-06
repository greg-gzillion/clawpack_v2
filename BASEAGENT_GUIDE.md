# BASEAGENT GUIDE — Clawpack V2

> READ THIS BEFORE WRITING ANY AGENT CODE.

Every agent inherits from BaseAgent. These methods already exist.
Stop reimplementing them. Use them.

---

## If your agent needs to call the LLM

```python
# WRONG — bypasses Sovereign Gateway, no budget tracking
import requests
resp = requests.post("http://127.0.0.1:8766/v1/message/llmclaw", ...)

# RIGHT — goes through Sovereign Gateway, budget-tracked
result = self.ask_llm("your prompt here")
```

`ask_llm()` routes through the Sovereign Gateway (Groq -> Ollama -> OpenRouter -> Anthropic).
All LLM access is constitutional. Chronicle context was removed from ask_llm() on June 4.

---

## If your agent needs retrieval (search)

```python
# BEST — cache-first with WebClaw BM25 fallback
result = self.cached_search(f"ns:{self.name} your query")
```

`cached_search()` provides:
- DataClaw cache check (24hr TTL, agents/dataclaw/cache/{agent}/)
- WebClaw BM25 fallback (provider + chronicle + dedup + source confidence)
- Automatic cache write for future queries
- Returns [CACHED] marker on cache hits
- Preserves score:, source:, deduped from markers

---

## If your agent needs to call another agent

```python
# WRONG — hardcoded HTTP, bypasses registry
import requests
r = requests.post("http://127.0.0.1:8766/v1/message/docuclaw", ...)

# RIGHT — constitutional cross-agent call with circuit breaker
result = self.call_agent("docuclaw", "/create my content", timeout=60)
result = self.call_agent("plotclaw", "/plot my data", timeout=30)
result = self.call_agent("webclaw", "fetch https://...", timeout=20)
```

`call_agent()` handles errors, timeouts, circuit breaker, and logging automatically.
Returns string on success, empty string on failure — always check before using.

---

## If your agent needs Chronicle (indexed knowledge)

```python
# Search 448MB Chronicle SQLite FTS5 index
results = self.search_chronicle("query terms", limit=10)
for r in results:
    ctx = r.get("context", "") if isinstance(r, dict) else str(r)
```

Chronicle has everything webclaw has ever fetched. 35,000+ indexed records.
Civic lookups return in 0.03-0.28s with zero LLM calls.

---

## If your agent needs to cache/retrieve results

```python
# Store a result to DataClaw cache
self.cache_result("agentname", "query", "results text")

# Retrieve from DataClaw cache
cached = self.get_cached_result("agentname", "query")
```

Cache location: agents/dataclaw/cache/{agent}/{query_hash}.json
24-hour TTL, automatic hit counting, JSON format.

---

## If your agent needs to log an error

```python
# WRONG — silent failure, UNCONSTITUTIONAL
except:
    pass

# RIGHT — constitutional audit logging
from shared._agent_helpers import log_err
log_err("agentname", "context", str(e)[:200])
```

---

## The methods every agent should use

| Need | Method | Notes |
|------|--------|-------|
| Call LLM | `self.ask_llm(prompt)` | Sovereign Gateway, budget-tracked |
| Retrieval | `self.cached_search(query)` | Cache-first, BM25 fallback, auto-cache |
| Call agent | `self.call_agent(name, task)` | Constitutional, circuit breaker |
| Search indexed | `self.search_chronicle(query)` | 448MB SQLite FTS5 |
| Cache result | `self.cache_result(agent, query, results)` | DataClaw cache |
| Get cached | `self.get_cached_result(agent, query)` | DataClaw cache |
| Log error | `log_err(agent, context, error)` | Constitutional audit |

---

## What BaseAgent gives you for free

- `self.name` — agent name string
- `self.state` — agent state dict (persisted)
- `self.track_interaction()` — increment interaction counter
- `self.call_agent()` — cross-agent with circuit breaker
- `self.ask_llm()` — Sovereign Gateway access
- `self.cached_search()` — cache-first retrieval
- `self.search_chronicle()` — FTS5 knowledge base
- `self.get_cached_result()` / `self.cache_result()` — DataClaw cache ops

---

## Minimal correct agent handler

```python
from shared.base_agent import BaseAgent
from shared._agent_helpers import log_err

class MyClawHandler(BaseAgent):
    def __init__(self):
        super().__init__("myclaw")

    def _gather_context(self, query=""):
        web = self.cached_search(f"ns:myclaw {query}")
        return str(web) if web else ""

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        try:
            if task.startswith("/search"):
                return {"status": "success", "result": self._gather_context(task[8:])}
            context = self._gather_context(task)
            result = self.ask_llm(f"{task}\n\nContext:\n{context}")
            return {"status": "success", "result": result}
        except Exception as e:
            log_err("myclaw", "handle", str(e)[:200])
            return {"status": "error", "result": str(e)}

_agent = MyClawHandler()
def process_task(task: str, agent: str = None):
    return _agent.handle(task)
```

---

## Provider Chain (June 5, 2026)

| Priority | Provider | Model | Latency | Cost |
|----------|----------|-------|---------|------|
| 1 | Groq | llama-3.3-70b-versatile | 0.7s | Free tier |
| 2 | Ollama | gemma3:4b | 0.8s GPU | Free (local) |
| 3 | OpenRouter | google/gemma-4-26b-a4b-it:free | 0.7s | Free tier |
| 4 | Anthropic | claude-haiku-4-5-20251001 | 1.2s | Paid |

Switch: llmclaw> /use groq

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| `import requests` + direct LLM call | `self.ask_llm()` |
| `import requests` + direct agent call | `self.call_agent()` |
| `call_agent("webclaw", ...)` for search | `self.cached_search()` |
| `except: pass` | `log_err("agent", "ctx", str(e))` |
| Using `str(PROJECT_ROOT)` literal | `Path(__file__).resolve().parent...` |
| Not passing `agent=self` to commands | Pass it — commands need context |
| Loading references at init | Use cached_search() — references are in Chronicle |
