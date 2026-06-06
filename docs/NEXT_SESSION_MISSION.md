# NEXT SESSION MISSION - Clawpack V2

## Read this before doing anything else
1. python scripts/scan.py
2. python scripts/onboard.py
3. docs/KNOWN_TRAPS.md
4. CLAWPACK_ONBOARD.md  <-- YOUR PRIMARY REFERENCE

## Current State (June 5, 2026 End of Session)

- **Validation**: 21/21 agents pass
- **Provider**: Groq primary (llama-3.3-70b-versatile, 0.7s, free)
- **BM25**: Retrieval engine stable. 9 agents show markers, 12 route through LLM
- **Cache**: Infrastructure exists (shared/search_cache.py). Only lawclaw populated.
- **Ledger**: Repaired. No lifecycle errors.
- **TxClaw**: Complete. 135 docs.tx.org URLs, 529 local files, cached_search wired.
- **Mediclaw**: Complete. 91 specialties, /hospital with GPS/URLs, cached_search wired.
- **DocuClaw/ClawCoder**: cached_search wired in _gather_context().

## Priority 1: Cache Population (HIGHEST PRIORITY)

cached_search() exists and works. Only lawclaw has cache entries.
Goal: WebClaw -> DataClaw cache -> local-first retrieval for all agents.

### Debug Checklist
```
# Check current cache state
python -c "from shared.search_cache import get_cache_stats; import json; print(json.dumps(get_cache_stats(), indent=2))"

# List cache directories
Get-ChildItem agents\dataclaw\cache -Recurse

# Verify cached_search exists
python -c "from shared.base_agent import BaseAgent; print(hasattr(BaseAgent, 'cached_search'))"
```

Verify each step: cached_search() called -> cache_result() called -> directory
created -> file written -> hit occurs -> hit count increments.

Investigate why agents calling cached_search() (mediclaw, txclaw, docuclaw,
claw_coder) aren't creating cache directories under agents/dataclaw/cache/.

## Priority 2: BM25 Visibility

BM25 markers (score:, source:, deduped from) exist in retrieval context
but ask_llm() converts them to natural language. 12 agents show as
"non-search" in validation because markers never reach the response.

Recommended: split-command approach
- /search -> return raw retrieval output with BM25 markers
- Normal requests -> retrieval context -> ask_llm() -> natural language

## Priority 3: _gather_context() Migration

12 agents still use raw call_agent('webclaw', ...) instead of cached_search().
Pattern is established. Replace in _gather_context() one agent at a time:

```python
# Before:
web = self.call_agent("webclaw", f"search ns:{agent} {query}", timeout=15)

# After:
web = self.cached_search(f"ns:{agent} {query}")
```

Test after each agent: restart server, run validate_agents.py, verify 21/21.
Check cache stats to confirm directory creation and hit counting.

### Migration Order
| Tier | Agents |
|------|--------|
| 1 (done) | txclaw, docuclaw, claw_coder |
| 2 (next) | draftclaw, crustyclaw, mathematicaclaw |
| 3 | drawclaw, plotclaw, flowclaw |
| Skip | fileclaw, llmclaw (no retrieval needed) |

## Priority 4: FlowClaw Consolidation

13 flowclaw*.py variants inventoried. Dependency map done.
agent_handler.py imports engine/, viewer/, exporters/ — those are canonical.
Archive the unused variants. Risk: MEDIUM. Follow FLOWCLAW RULE: no deletions
in first session, read-only inventory first.

## Priority 5: Enforcement Activation

Detection works (6 sovereignty patterns blocked at HTTP boundary).
Full EnforcementEngine (PreExecutionGate, PostExecutionGate) is DORMANT.
Activate: wire enforcement/engine.py and enforcement/gates.py into A2A path.

## After Any Shared Module Change

1. Delete __pycache__: Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
2. Compile: python -c "compile(open('file.py').read(),'file.py','exec'); print('OK')"
3. Validate: python scripts/validate_agents.py
4. Verify 21/21 pass
5. Check cache: python -c "from shared.search_cache import get_cache_stats; print(get_cache_stats())"

## Key Reference Files

| File | Purpose |
|------|---------|
| CLAWPACK_ONBOARD.md | Primary reference — architecture, state, debug checklists |
| docs/KNOWN_TRAPS.md | Mistakes that cost hours |
| POWERSHELL_SURVIVAL_GUIDE.md | How to write files in this environment |
| docs/WEBCLAW_MANUAL.md | WebClaw complete guide |
| docs/WEBCLAW_ARCHITECTURE.md | WebClaw system design |
| scripts/validate_agents.py | 21-agent validation harness |
