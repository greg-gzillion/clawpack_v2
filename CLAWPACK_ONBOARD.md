# CLAWPACK V2 — AI ONBOARDING CONTEXT

## What This Is
21-agent AI ecosystem. Menu-driven CLI. A2A routing on port 8766.
448MB Chronicle SQLite index at runtime/chronicle.db. Constitutional governance.
Built by Greg.

## RUN THIS FIRST
`python scripts/onboard.py` — prints everything you need to understand this system.
`python scripts/validate_agents.py` — tests all 21 agents against V2 retrieval semantics.
CRITICAL: Read docs/KNOWN_TRAPS.md before writing any code.
Also read: docs/READ_THIS_FIRST.md for quick start.
Also read: docs/WEBCLAW_MANUAL.md for the complete WebClaw guide.

## CRITICAL: How to Write Files in This Environment

### The ONLY safe method: Pattern B (Python builder script)
1. Write a Python script that builds the target file as a list of lines
2. Save to scripts/_temp.py, run it, verify syntax, delete builder
3. Clear __pycache__ after shared module changes

### What NEVER works:
- python -c with multi-line code (quotes mangle)
- PowerShell heredocs with Python (quotes conflict)
- echo appending (UTF-16 BOM breaks imports)
- Pasting Python directly into PowerShell terminal

## Constitution (NON-NEGOTIABLE)
- All LLM access through Sovereign Gateway only (shared/llm/client.py)
- All exceptions must log. except: pass is UNCONSTITUTIONAL.
- Truth hierarchy: web_verified > chronicle > memory > inference.
- Every agent has defined jurisdiction. No crossing.
- Command files for deployment. Never inject into handlers.

---

## RETRIEVAL ARCHITECTURE MAP (AUTHORITATIVE)

```
User Query
    ↓
Agent Handler
    ↓
_gather_context()
    ↓
cached_search()  [TARGET ARCHITECTURE]
    ↓
DataClaw Cache (agents/dataclaw/cache/{agent}/)
    ↓ (miss)
WebClaw BM25 (provider + chronicle + merge + dedup)
    ↓
Chronicle FTS5 (runtime/chronicle.db, 448MB)
    ↓
final_score = bm25_score * source_weight
    ↓
Context returned to agent
    ↓
ask_llm() [BM25 markers stripped here]
    ↓
Response
```

**Current Reality**: Some agents still bypass cached_search() and call
WebClaw directly. Some access Chronicle directly. Only lawclaw cache
is actively populated. Both paths work — output format differs.

---

## CHRONICLE FACTS

| Fact | Value |
|------|-------|
| Database | runtime/chronicle.db |
| Size | ~448 MB |
| Engine | SQLite FTS5 |
| Purpose | Primary local knowledge layer |
| Contains | TX references, medical references, legal references, cached artifacts, agent memory |
| Search APIs | search_chronicle(), BM25 retrieval, FTS5 indexes |
| ⚠️ WARNING | Never rebuild casually. Treat as production data. |

---

## Current State — June 5, 2026 (End of Session)

### Validation: 21/21 AGENTS PASS
All agents respond. Harness adjusted for txclaw query format.
Constitutional ledger corruption fixed. Lifecycle cleanup errors resolved.

### Two Agent Classes Discovered

**BM25 agents (9)**: Return raw retrieval with score/source/dedup markers.
lawclaw, claw_coder, crustyclaw, designclaw, dreamclaw, interpretclaw,
langclaw, liberateclaw, webclaw

**Non-search agents (12)**: Route retrieval through ask_llm() which strips
BM25 markers. mediclaw, draftclaw, dataclaw, drawclaw, flowclaw, docuclaw,
llmclaw, mathematicaclaw, plotclaw, rustypycraw, txclaw, fileclaw

**Key insight**: BM25 markers exist in retrieval context but ask_llm() converts
them to natural language. Both paths WORK — just different output format.

---

## AGENT RETRIEVAL CLASSIFICATION

| Priority | Agents |
|----------|--------|
| HIGH (need retrieval) | lawclaw, mediclaw, txclaw, docuclaw, claw_coder |
| MEDIUM | draftclaw, crustyclaw, mathematicaclaw |
| LOW | drawclaw, plotclaw, flowclaw |
| NONE | fileclaw, llmclaw |

---

## KNOWN ARCHITECTURAL DEBT

| Issue | Severity | Detail |
|-------|----------|--------|
| Cache population incomplete | HIGH | Only lawclaw has cache entries |
| Multiple retrieval patterns | MEDIUM | cached_search(), direct WebClaw, direct Chronicle |
| claw_coder WebClawClient | LOW | Dead code, port 5000 legacy, 39 language imports |
| BM25 visibility inconsistent | LOW | Retrieval works, output format differs by agent |
| FlowClaw 13 variants | MEDIUM | Inventory done, consolidation pending |
| Enforcement blocking | MEDIUM | Detection active, blocking dormant |

---

## CACHE DEBUG CHECKLIST

```
# Check cache stats
python -c "from shared.search_cache import get_cache_stats; import json; print(json.dumps(get_cache_stats(),indent=2))"

# List cache directories
Get-ChildItem agents\dataclaw\cache -Recurse

# Verify cached_search exists
python -c "from shared.base_agent import BaseAgent; print(hasattr(BaseAgent,'cached_search'))"
```

Verify: cached_search() called → cache_result() called → directory created →
file written → hit occurs → hit count increments

---

## DANGEROUS FILES (modify only with validation afterwards)

| File | Risk |
|------|------|
| shared/base_agent.py | All 21 agents inherit from this |
| shared/search_cache.py | Cache infrastructure for entire system |
| shared/llm/client.py | Sovereign Gateway — Article I |
| agents/webclaw/agent_handler.py | Retrieval pipeline orchestration |
| runtime/chronicle.db | 448MB production data — never rebuild casually |
| runtime/ledgers/constitutional_ledger.json | Audit trail integrity |

---

## MANDATORY VALIDATION AFTER SHARED MODULE CHANGES

1. Delete __pycache__: Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
2. Compile: python -c "compile(open('file.py').read(),'file.py','exec'); print('OK')"
3. Run harness: python scripts/validate_agents.py
4. Verify 21/21 pass
5. Check cache: python -c "from shared.search_cache import get_cache_stats; print(get_cache_stats())"

---

## WebClaw V2 Retrieval Engine (STABLE)
BM25 + source confidence authoritative ranking. Dedup by URL at merge boundary.
Context truncation: 300 -> 10000 chars. Cache truncation removed at all 3 layers.

## TxClaw — COMPLETE
117 lines. TX.org-exclusive. cached_search() wired.
DataClaw: 529 files/17 domains. WebClaw: 135 docs.tx.org URLs/11 domains.

## Mediclaw — COMPLETE
177 lines. Groq primary. /hospital returns name/address/phone/website/GPS.
/sources shows 91 specialties. cached_search() wired. str(PROJECT_ROOT) fixed.

## LLMClaw — UPDATED
/use supports groq/openrouter/anthropic. Active: llama-3.3-70b-versatile (groq).

## APIs Verified
Groq: 200 | OpenRouter: 200 | Anthropic: SET | CourtListener: SET (as TOKEN)

---

## Key Changes Today

| File | Change |
|------|--------|
| shared/search_cache.py | Removed results[:5000] truncation |
| shared/base_agent.py | Removed cached['results'][:3000] truncation |
| agents/webclaw/agent_handler.py | ctx[:300] -> ctx[:10000] |
| agents/mediclaw/agent_handler.py | Handler patched, cached_search wired |
| agents/mediclaw/commands/_helpers.py | Hospital parser uses cached_search |
| agents/mediclaw/core/engine.py | Fixed str(PROJECT_ROOT) |
| agents/txclaw/agent_handler.py | cached_search wired |
| agents/docuclaw/agent_handler.py | cached_search wired |
| agents/claw_coder/agent_handler.py | cached_search wired (both calls) |
| agents/llmclaw/commands/use.py | Cloud provider support |
| agents/llmclaw/commands/list.py | Cloud providers in model list |
| runtime/ledgers/constitutional_ledger.json | Fixed duplicate tail corruption |
| agents/dataclaw/references/* | 21 agent directories created |
| scripts/validate_agents.py | Harness created, txclaw query fixed |

---

## Next Session Mission

1. **Cache population** — cached_search() works but only lawclaw has entries.
   Use Cache Debug Checklist above. Goal: all retrieval agents populating cache.
2. **BM25 visibility** — Split /search (raw retrieval) from normal requests (LLM).
3. **_gather_context() migration** — 12 agents still use raw call_agent('webclaw').
4. **FlowClaw consolidation** — 13 variants -> 1, inventory done.
5. **Enforcement activation** — detection works, blocking dormant.

---

## Beta Gate Progress

| # | Requirement | Status |
|---|-------------|--------|
| 1 | Enforcement blocks violations | DONE |
| 2 | 21 agents online | DONE |
| 3 | Constitutional ledger stable | DONE |
| 4 | WebClaw BM25 operational | DONE |
| 5 | Validation harness operational | DONE |
| 6 | Cache population working | IN PROGRESS |
| 7 | Retrieval standardization | IN PROGRESS |
| 8 | FlowClaw consolidation | TODO |
| 9 | Enforcement activation | TODO |
| 10 | Beta readiness review | TODO |
