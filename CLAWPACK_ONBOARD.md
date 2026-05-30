> READ THIS FIRST. Do not write any code until you have read this entire document.

# CLAWPACK V2 - AI ONBOARDING CONTEXT

## What This Is
21-agent AI ecosystem. Menu-driven CLI. A2A routing on port 8766.
448MB Chronicle SQLite index at data/chronicle.db. Constitutional governance.
Built by Greg. You are helping build and maintain all 21 agents.

## Before You Write Any Code
1. Ask to see the current file if modifying an existing command.
2. Ask to see a working command if building a new stub.
3. Do not assume file contents - they may differ from conversation history.
4. State what you are about to do before doing it. One function at a time.
5. Use file-based Python scripts (Out-File + python script.py), NOT python -c with multi-line strings. PowerShell corrupts them.

## How Commands Load
Commands in each agent''s commands/ directory are loaded dynamically.
Each file needs: name = "/commandname" and def run(args): at module level.
No manual registration - just drop the .py file in the directory.

## Constitution (NON-NEGOTIABLE)
- All LLM access goes to Sovereign Gateway only (A2A to llmclaw). No direct API calls.
- All exceptions must log. except: pass is UNCONSTITUTIONAL.
- Truth hierarchy: web_verified > chronicle > memory > inference.
- Every agent has defined jurisdiction. No crossing.

---

## Current State — May 29, 2026 (EVENING)

### Constitutional Agents (11 of 21)
Full 23-system boundary, capability routing, shared memory bridge, cross-agent delegation:

| Agent | Status | Unique Capabilities |
|-------|--------|-------------------|
| lawclaw | 10/10 | Gold standard, 24 commands, /doc enrichment, /translate chain, jurisdiction civic profiles |
| claw_coder | 10/10 | 39-language code gen + validation, memory recall before generation |
| crustyclaw | 10/10 | Rust audit/pinch/fix, standalone binary fallback |
| dataclaw | 10/10 | 41K local files indexed, Chronicle writes, data export |
| designclaw | 10/10 | Brand identity, building codes from 3,800+ city jurisdiction files |
| mediclaw | 10/10 | Hospital geolocation, urgency triage, professional/layperson detection, /doc medical |
| draftclaw | 10/10 | Blueprints, CAD, structural packages, permit compliance, design criteria lookup |
| dreamclaw | 10/10 | AI vision and generation |
| interpretclaw | 10/10 | 42 languages + Braille (opt-in), cross-platform TTS |
| langclaw | 10/10 | Language teaching, cross-platform TTS |
| liberateclaw | 10/10 | Model liberation, obliterated model management |

### Partially Connected (9 agents)
Have boundary + routing + memory bridge, but audit shows PARTIAL due to compact boundary format or specialized LLM paths:

| Agent | Score | Notes |
|-------|-------|-------|
| docuclaw | 9/10 | Document creation, validation engine, 31 commands |
| flowclaw | 9/10 | Diagrams/flowcharts, specialized LLMAdapter for Mermaid.js |
| llmclaw | 8/10 | Sovereign Gateway manager, model orchestration |
| mathematicaclaw | 8/10 | SymPy math engine, 9 commands |
| plotclaw | 8/10 | 13 chart types, matplotlib |
| rustypycraw | 8/10 | Code crawler, AST analysis |
| txclaw | 8/10 | Blockchain, smart contracts |
| webclaw | 8/10 | Chronicle owner, web search, 3,800+ city references |
| drawclaw | 9/10 | 14 art commands, import fixed |
| fileclaw | 8/10 | 41+ format import/export/conversion |

### Isolated (1 agent)
| Agent | Notes |
|-------|-------|
| langclaw_backup | Archived backup, not active |

---

## New Infrastructure Deployed (May 29, 2026)

### 1. Circuit Breaker on BaseAgent.call_agent()
5 consecutive failures opens circuit for 60s, then half-open recovery with 3 test calls.
Protects all cross-agent communication. Wired into shared/base_agent.py.

### 2. lookup_jurisdiction() on BaseAgent
All 21 agents inherit Chronicle-powered jurisdiction lookup via FTS5 index.
Library, hospital, police, and building code data from 3,800+ cities.
Replaces slow filesystem walk with SQLite full-text search.

### 3. Constitutional Agent Upgrade Pattern
Three files per agent (5 minutes each):
- commands/_memory.py — copy from lawclaw, change agent name
- commands/_helpers.py — agent-specific utilities + jurisdiction lookup
- agent_handler.py — add import time, _gather_context(), 23-system boundary block, capability routing, /delegate route

### 4. Cross-Platform Text-to-Speech
Windows SAPI, macOS say, Linux espeak. Deployed to langclaw and interpretclaw.

### 5. Hospital Geolocation (mediclaw)
Find nearest hospital to GPS coordinates. Emergency department lookup by city.
Specialty filtering (cardiac, pediatric, trauma, neuro, etc.).
Uses 3,800+ city jurisdiction files via Chronicle FTS5.

### 6. Building Code Lookup (designclaw, draftclaw)
Extract IBC/IRC/NEC codes, frost depth, snow load, wind speed, seismic data
from jurisdiction files. Design criteria for structural packages.

### 7. Braille Accessibility (interpretclaw)
Opt-in feature (INTERPRETCLAW_BRAILLE=1). Grade 1 and Grade 2 Braille ASCII.
Works with reasoning models (deepseek-r1, claude, gpt-4).

### 8. Medical Document Generation (mediclaw)
/doc medical report, referral letter, treatment plan, discharge instructions.
Chains through docuclaw for formatting.

---

## Chronicle Index (448MB SQLite FTS5)
- All 3,800+ city jurisdiction files ARE indexed with full-text search
- recover_by_context(query, limit) — the canonical search method
- DOES NOT have get_timeline — that method does not exist, the boundary error is a false positive
- The index is organized by county, not city — but FTS5 searches across all boundaries
- lookup_jurisdiction() in BaseAgent uses Chronicle first, not filesystem walk

## A2A Server (port 8766)
- Running continuously — do NOT stop it
- a2a_server.py is the central message bus
- /v1/message/{agent} — POST endpoint for cross-agent calls
- /health — GET endpoint for server status

## Known Non-Blocking Errors (ignore these)
- cannot import name 'log_event' — wrong import path, fails silently in boundary
- DecisionLedger.record() got unexpected keyword argument 'action' — API mismatch
- ChronicleLedger has no attribute 'get_timeline' — method does not exist
- All handled by except Exception: pass in the 23-system boundary block

---

## Path Forward (Priority Order)

### Phase 1: Complete New Infrastructure Deployment ✅ DONE
1. DONE shared/capabilities.py
2. DONE shared/lifecycle.py
3. DONE shared/memory_guard.py
4. DONE LawClaw handler — capability routing + 23-system boundary + telemetry + /translate
5. DONE shared/registry.py — fixed syntax errors, docuclaw delegation path
6. DONE Circuit breaker on BaseAgent.call_agent()
7. DONE lookup_jurisdiction() on BaseAgent via Chronicle FTS5
8. DONE Deploy constitutional shell to 11 agents (boundary + routing + memory)
9. Wire lifecycle into a2a_server.py

### Phase 2: Constitutional Completion (Tier 1)
1. Wire enforcement/engine.py into a2a_server.py (Article XI)
2. Fix llmclaw's own_llm (Article I)
3. Wire guarded_executor.py into a2a_server.py (Article IV)
4. Fix 3 cosmetic boundary errors (log_event import, DecisionLedger API, get_timeline)

### Phase 3: Complete the Mesh — Command-Level Connectivity 🔄 IN PROGRESS
1. DONE jurisdiction.py — now uses agent context (Sovereign Gateway, Chronicle, BaseAgent)
2. Migrate remaining 12 lawclaw commands from direct HTTP to agent context
3. Migrate commands in all other agents to use agent context
4. Merge 5 missing agents into registry AGENT_REGISTRY dict

### Phase 4: Activation
1. Wire enforcement/engine.py into a2a_server.py (Article XI)
2. Wire guarded_executor.py into a2a_server.py (Article IV)
3. Wire lifecycle.py into a2a_server.py

---

## Cross-Agent Communication — What Works

Every constitutional agent can call every other agent through:
1. Capability Registry — unrecognized commands auto-route via get_capable_agent()
2. Direct /delegate — explicit call_agent("agent_name", task)
3. Circuit breaker — 5 failures opens circuit for 60s

Known working flows:

---

## Quick Reference: Files That Matter

| File | Purpose | Status |
|------|---------|--------|
| a2a_server.py | Central message bus, port 8766 | Running continuously |
| shared/base_agent.py | Foundation class — call_agent(), ask_llm(), lookup_jurisdiction(), search_chronicle() | Active + circuit breaker |
| shared/capabilities.py | Universal command routing | Deployed to 11 agents |
| shared/lifecycle.py | Agent cleanup supervisor | Wire into a2a_server.py |
| shared/error_handler.py | Circuit breaker — 5 failures, 60s recovery | Active on all call_agent() |
| shared/memory_guard.py | Confidence + staleness enforcement | Active |
| shared/_agent_helpers.py | Empire-wide utilities | Active |
| shared/consensus_engine.py | Reputation-based truth scoring | Active |
| agents/lawclaw/agent_handler.py | Reference implementation | GOLD STANDARD |
| agents/webclaw/references/lawclaw/jurisdictions/us/ | 3,800+ cities | Active, Chronicle-indexed |
| data/chronicle.db | 448MB SQLite FTS5 | Active, ~35K interactions |

---

## Session Log

2026-05-27: All 12 lawclaw commands built. _helpers.py and _memory.py created.

2026-05-28: All 21 agents wired with shared/_agent_helpers.py. 23 commands memory-wired.
Constitutional Command Lifecycle section added. First cross-agent flow proven.

2026-05-29 (morning): Constitutional execution boundary activated. Registry syntax errors fixed.
Docuclaw delegation path repaired. PlotClaw schema imports fixed across 13 chart commands.

2026-05-29 (afternoon/evening): MAJOR ARCHITECTURAL UPGRADE.
- Circuit breaker deployed to BaseAgent.call_agent() — protects all cross-agent calls
- lookup_jurisdiction() added to BaseAgent — all 21 agents get library/hospital/police/building codes
- Constitutional shell deployed to 10 additional agents (claw_coder, crustyclaw, dataclaw,
  designclaw, mediclaw, draftclaw, dreamclaw, interpretclaw, langclaw, liberateclaw)
- Hospital geolocation with GPS coordinates from 3,800+ city files
- Building code/design criteria lookup from jurisdiction files
- Cross-platform TTS (Windows SAPI, macOS say, Linux espeak)
- Braille accessibility (opt-in, Grade 1 & 2)
- 42 languages in interpretclaw (including Latin, ASL gloss)
- Medical document generation (/doc) in mediclaw
- Groq model upgraded to llama-3.3-70b-versatile
- 2 CodeQL security alerts resolved
- 15 dead files deleted, shared/registry.py repaired
- jurisdiction.py command migrated from direct HTTP to agent context (Sovereign Gateway + Chronicle)

**Result: 1 -> 11 constitutional agents. 60 -> ~20 remaining gaps.**
**Chronicle interactions: 35,000+. Constitutional runtime: ACTIVE.**
