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

The PowerShell terminal and Python have conflicting string delimiters.
Directly pasting Python code into PowerShell WILL FAIL. Every time.

### The ONLY safe method: Pattern B (Python builder script)
1. Write a Python script that builds the target file as a list of lines
2. Save the builder script to disk (scripts/_temp.py)
3. Run it: python scripts/_temp.py
4. Verify: python -c "compile(open('target.py').read(),'target.py','exec'); print('Syntax OK')"
5. Delete the builder: Remove-Item scripts/_temp.py -Force

Example builder pattern:
```python
from pathlib import Path
L = []
L.append('line 1')
L.append('line 2')
Path('output.py').write_text('\n'.join(L) + '\n', encoding='utf-8')
print(f'Wrote {len(L)} lines')
```

### What NEVER works:
- python -c with multi-line code (nested quotes mangle)
- PowerShell heredocs containing Python code (quotes conflict)
- echo appending for multi-line content (UTF-16 BOM breaks imports)
- Out-File for files over ~100 lines (silent truncation)
- Pasting Python code directly into PowerShell terminal

### After any shared module change:
```powershell
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
taskkill /F /IM python.exe 2>$null
```

## Constitution (NON-NEGOTIABLE)
- All LLM access goes to Sovereign Gateway only (shared/llm/client.py). No direct API calls.
- All exceptions must log. except: pass is UNCONSTITUTIONAL.
- Truth hierarchy: web_verified > chronicle > memory > inference.
- Every agent has defined jurisdiction. No crossing.
- Command files for deployment. Never inject into handlers.

---

## Current State — June 5, 2026

### WebClaw V2 Retrieval Engine (STABLE)
BM25 + source confidence is the authoritative ranking layer over merged provider + Chronicle results.
Deduplication by URL at the merge boundary. Namespace scoping (ns:agent) active on all agents.
All V1 artifacts removed (config.py, shared_memory.py, api.py, webclaw_agent.py, provider_backup.py).
Agent handler: 135 lines (was 237). Constitutional boundary dead block removed.

Retrieval pipeline:
```
provider.search_structured() -> chronicle.recover_by_context() -> merge + dedup by URL
    -> BM25.index() -> BM25.search() -> final_score = bm25_score * source_weight
```

source_registry is documented as a global ranking governor — changing trust values
affects retrieval order for all 21 agents.

### DataClaw — Local Data Retrieval
DataClaw serves local structured data using the same namespace-scoped pattern as WebClaw.
DataClaw = static truth storage. WebClaw = runtime intelligence. Separate entities.
TxClaw local corpus: 529 files across 17 domains in agents/dataclaw/references/txclaw/
WebClaw txclaw online references: 61 files across 17 domains, TX.org-exclusive URLs.

### Agent Validation (June 5, 2026)
13 agents pass V2 retrieval validation. 8 agents fail:

| Agent | Failure | Likely Cause |
|-------|---------|-------------|
| mediclaw | Timeout >60s | Slow LLM inference |
| draftclaw | Timeout >60s | Heavy processing |
| dataclaw | Timeout >60s | Local file search |
| drawclaw | Timeout >60s | Untested handler |
| docuclaw | Timeout >60s | 3 implementations |
| plotclaw | Timeout >60s | Untested |
| rustypycraw | Timeout >60s | Direct Groq import, multi-agent calls |
| txclaw | Empty response | Handler loads 470 files at init |

TxClaw handler has been patched (117 lines, was 200+). Now queries DataClaw for local
docs and WebClaw for web search. Removed _load_references() preloading.

### Runtime Health
| Metric | Value |
|--------|-------|
| Agent availability | 21/21 responsive |
| A2A transport | Healthy (port 8766) |
| Chronicle index | 35,000+ interactions |
| LLM providers | Ollama, Groq, OpenRouter, Anthropic |
| Active model | gemma3:4b (Ollama) |
| Provider chain | Ollama -> Groq -> OpenRouter -> Anthropic |
| Enforcement | 6 sovereignty patterns blocked at HTTP boundary (403) |
| BM25 retriever | Wired into production query path |
| Namespace scoping | Active on all agents |
| Deduplication | URL-based at merge boundary |

### WebClaw Cleanup Summary (June 5, 2026)
| Action | Result |
|--------|--------|
| core/api.py | Deleted (zero consumers) |
| core/config.py | Deleted (V1, hardcoded path) |
| core/shared_memory.py | Deleted (V1 memory system) |
| webclaw_agent.py | Deleted (standalone CLI variant) |
| a2a/integrated_server.py | Deleted (FastAPI stub) |
| providers/webclaw_provider_backup.py | Deleted (bitmap provider) |
| TETHERED_SYSTEM_DOCUMENTATION.md | Archived (V1 docs) |
| 6 commands | Migrated V1->V2 (Chronicle + path resolution) |
| Constitutional boundary block | 102 lines removed from handler |
| BM25 retriever | Wired, verified live with [score: X.XXX, source: X.XX] |
| Deduplication | Active (Found X results deduped from Y candidates) |
| search_structured() | Added to WebclawProvider for BM25 document schema |

### TxClaw Architecture
TxClaw is exclusive to the TX.org blockchain. Two-layer knowledge architecture:

| Layer | Location | Contents | Role |
|-------|----------|----------|------|
| DataClaw | agents/dataclaw/references/txclaw/ | 529 files, 17 domains | Local documentation |
| WebClaw | agents/webclaw/references/txclaw/ | 61 files, 17 domains | Online references |

17 domains: api, architecture, assets, blockchain, development, dex, ecosystem,
governance, ibc, introduction, modules, nodes, regulatory, security, services,
smart_contracts, tutorials.

TxClaw handler queries DataClaw for local docs and WebClaw for web search.
No file preloading. No 2M Chronicle limit. No constitutional boundary dead block.

### Key Files
| File | Purpose | Status |
|------|---------|--------|
| a2a_server.py | Central message bus, port 8766 | Active |
| shared/llm/client.py | Sovereign Gateway | Active |
| shared/base_agent.py | Foundation class for all 21 agents | Active |
| agents/webclaw/agent_handler.py | WebClaw A2A handler, BM25 orchestration | Active (135 lines) |
| agents/webclaw/providers/webclaw_provider.py | SQLite search, namespace scoping, search_structured() | Active (139 lines) |
| agents/webclaw/core/retriever.py | BM25 ranking, source confidence (global ranking governor) | Active |
| agents/webclaw/core/chronicle_ledger.py | Chronicle FTS5, recover_by_context, record_fetch | Active |
| agents/dataclaw/references/txclaw/ | TX.org local documentation (529 files, 17 domains) | Active |
| agents/webclaw/references/txclaw/ | TX.org online references (61 files, 17 domains) | Active |
| agents/dataclaw/commands/_helpers.py | Local file search + DataClaw reference path | Active |
| agents/dataclaw/commands/data.py | Namespace-scoped search, DataClaw citation tags | Active |
| agents/txclaw/agent_handler.py | TxClaw handler (DataClaw + WebClaw context) | Active (117 lines) |
| scripts/validate_agents.py | 21-agent validation harness | Active |
| docs/WEBCLAW_MANUAL.md | Comprehensive WebClaw guide (updated) | Active |
| docs/WEBCLAW_ARCHITECTURE.md | WebClaw system design with diagram | Active |
| runtime/chronicle.db | 448MB SQLite FTS5 | Active |

### Next Session Mission
Priority order based on operational risk:

1. **Failing agents**: mediclaw, draftclaw, docuclaw, dataclaw, drawclaw, plotclaw, rustypycraw
   - Determine which are genuinely broken vs. slow inference vs. need different validation
2. **FlowClaw consolidation**: 13 variants -> 1, inventory done, ready for archive phase
3. **WebClaw txclaw URL population**: Verify and populate live URLs in reference files
4. **Enforcement activation**: Detection works, blocking dormant (largest security gap)
5. **Archive cleanup**: TETHERED_SYSTEM_DOCUMENTATION.md already archived

### Beta Gate Progress (5/10)
| # | Requirement | Status |
|---|-------------|--------|
| 1 | Enforcement blocks violations | DONE |
| 2 | Constitutional ledger repaired | DONE |
| 3 | Memory geographic filtering | DONE |
| 4 | All 21 agents tested | DONE (13 pass, 8 fail documented) |
| 5 | Provider fallback validated | DONE |
| 6 | Duplicate implementations reduced | IN PROGRESS (WebClaw done, TxClaw done, FlowClaw pending) |
| 7 | Coverage tests added | NOT STARTED |
| 8 | Clean Windows install tested | NOT STARTED |
| 9 | Clean Linux install tested | NOT STARTED |
| 10 | Security review completed | NOT STARTED |
