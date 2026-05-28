> READ THIS BEFORE WRITING ANY AGENT CODE.

# BASEAGENT GUIDE — Clawpack V2

Every agent inherits from BaseAgent. These methods already exist.
Stop reimplementing them. Use them.

---

## If your agent needs to call the LLM

```python
# WRONG — bypasses Sovereign Gateway, no budget tracking, no Chronicle enrichment
import requests
resp = requests.post("http://127.0.0.1:8766/v1/message/llmclaw", ...)

# RIGHT — goes through Sovereign Gateway, Chronicle-enriched, budget-tracked
result = self.ask_llm("your prompt here")

# BEST — full truth resolver pipeline (retriever + memory guard + conflict detection)
result = self.smart_ask("your prompt here")
```

`ask_llm()` automatically searches Chronicle before calling the LLM.
`smart_ask()` also runs the truth resolver and memory guard.
Both route through the Sovereign Gateway. Both are constitutional.

---

## If your agent needs to call another agent

```python
# WRONG — hardcoded HTTP, no error handling, bypasses registry
import requests
r = requests.post("http://127.0.0.1:8766/v1/message/docuclaw", ...)

# RIGHT — constitutional cross-agent call
result = self.call_agent("docuclaw", "/create my content", timeout=60)
result = self.call_agent("plotclaw", "/plot my data", timeout=30)
result = self.call_agent("webclaw", "fetch https://...", timeout=20)
result = self.call_agent("lawclaw", "/law qualified immunity", timeout=60)
```

`call_agent()` handles errors, timeouts, and logging automatically.
Returns empty string on failure — always check before using.

---

## If your agent needs to search the web

```python
# WRONG — direct HTTP, bypasses Chronicle indexing
import requests
r = requests.get("https://example.com", ...)

# RIGHT — goes through webclaw, indexed to Chronicle
result = self.search_web("query terms")           # returns formatted results
result = self.search_web_raw("query", max_results=20)  # raw results list
```

---

## If your agent needs to search what's already been indexed

```python
# RIGHT — search 448MB Chronicle SQLite index
results = self.search_chronicle("query terms", limit=10)
for r in results:
    ctx = r.get("context", "") if isinstance(r, dict) else str(r)
    url = r.get("url", "") if isinstance(r, dict) else ""
```

Chronicle has everything webclaw has ever fetched.
Search it before hitting external APIs.

---

## If your agent needs to remember something across sessions

```python
# Write a fact (persists to data/shared_memory.json)
self.learn("last_case_searched", "Miranda v Arizona")

# Read it back
last = self.recall("last_case_searched")

# Write to unified cross-agent memory (all 21 agents share this)
self.learn_fact("Qualified immunity requires clearly established rights")

# Read unified memory
facts = self.get_facts()
```

---

## If your agent needs to record something to Chronicle

```python
# Index a URL and its content to the 448MB Chronicle
self.record_in_chronicle(
    url="https://www.courtlistener.com/opinion/123/",
    context="Miranda v Arizona established Fifth Amendment warnings",
    source="lawclaw"
)
```

---

## If your agent needs to log an error

```python
# WRONG — silent failure
except:
    pass

# RIGHT — constitutional audit logging
except requests.exceptions.Timeout as e:
    self._log_error("fetch_timeout", str(e))
except Exception as e:
    self._log_error("fetch_error", str(e)[:200])
```

---

## The 5 methods every agent should use

| Need | Method | Notes |
|------|--------|-------|
| Call LLM | `self.ask_llm(prompt)` | Chronicle-enriched, budget-tracked |
| Call LLM + truth | `self.smart_ask(prompt)` | Full pipeline, conflict detection |
| Call another agent | `self.call_agent(name, task)` | Constitutional, error-handled |
| Search web | `self.search_web(query)` | Via webclaw, indexed to Chronicle |
| Search indexed | `self.search_chronicle(query)` | 448MB SQLite, fast |

---

## What BaseAgent gives you for free

- `self.A2A` — A2A server URL (http://127.0.0.1:8766)
- `self.memory` — UnifiedMemory instance (cross-agent)
- `self.webclaw` — WebclawProvider instance
- `self.state` — agent state dict (persisted to shared_memory.json)
- `self.name` — agent name string
- `self.track_interaction()` — increment interaction counter

---

## Minimal correct agent handler

```python
from shared.base_agent import BaseAgent

class MyClawHandler(BaseAgent):
    def __init__(self):
        super().__init__("myclaw")

    def handle(self, task: str) -> dict:
        self.track_interaction()
        try:
            # Use BaseAgent methods — don't reimplement them
            context = self.search_chronicle(task, limit=5)
            result = self.ask_llm(f"Answer this: {task}\n\nContext: {context}")
            return {"status": "success", "result": result}
        except Exception as e:
            self._log_error("handle_error", str(e))
            return {"status": "error", "result": str(e)}

_agent = MyClawHandler()
def process_task(task: str, agent: str = None):
    return _agent.handle(task)
```

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| `import requests` + direct LLM call | `self.ask_llm()` |
| `import requests` + direct agent call | `self.call_agent()` |
| `requests.get(url)` for web fetch | `self.search_web()` or `call_agent("webclaw", "fetch url")` |
| `except: pass` | `self._log_error("context", str(e))` |
| Defining own `_log()` function | `self._log_error()` already exists |
| Defining own `get_token()` | Read from `Path(".env")` or use `self.recall("token")` |
| Reimplementing Chronicle search | `self.search_chronicle(query)` |
