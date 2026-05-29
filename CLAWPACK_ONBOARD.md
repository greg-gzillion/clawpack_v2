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

## How Commands Load
Commands in each agent's commands/ directory are loaded dynamically.
Each file needs: name = "/commandname" and def run(args): at module level.
No manual registration - just drop the .py file in the directory.

## Constitution (NON-NEGOTIABLE)
- All LLM access goes to Sovereign Gateway only (A2A to llmclaw). No direct API calls.
- All exceptions must log. except: pass is UNCONSTITUTIONAL.
- Truth hierarchy: web_verified > chronicle > memory > inference.
- Every agent has defined jurisdiction. No crossing.

## Separation of Powers — Constitutional Citation Doctrine (May 29, 2026)

**Every document-producing agent must attribute its sources. This is constitutional law.**

| Ministry | Citation Responsibility |
|----------|------------------------|
| **WebClaw** | Source acquisition authority — fetches, indexes, attributes all URLs to Chronicle |
| **LawClaw/MedicLaw/TXClaw** | Domain enrichment authority — adds contextual intelligence to citations |
| **DocuClaw** | Document synthesis authority — reflects citations in Constitutional Source Validation block |
| **Constitutional Boundary** | Compliance enforcement authority — warns on incomplete provenance |

When a document is generated, the boundary SHALL verify:
1. DocuClaw's validation block is present ("Constitutional Source Validation")
2. Source URLs are included ("https://" in output)
3. If either is missing, a constitutional warning is appended

No new subsystem needed. The ministries already exist. The boundary enforces their cooperation.

---

## Current State — May 29, 2026

### LawClaw Utilization of Shared Infrastructure: 38 of 38 files (100%)

All 23 systems fire automatically on every command through the handler boundary.
LawClaw is the first agent to achieve full constitutional connectivity.

**Tier 1 — Constitutional Closure (4 systems):**
lifecycle.py, enforcement/engine.py, guarded_executor.py, execution_policy.py

**Tier 2 — Legal Cognition (3 systems):**
chronicle_helper.py, procedural_memory.py, three_tier.py

**Tier 3 — Multi-Agent Intelligence (2 systems):**
smart_router.py, agent_router.py

**Tier 4 — Operational Polish (4 systems):**
validation.py, log_manager.py, shutdown.py, hooks/

**Existing Active Systems (10):**
budget check, rate limit, circuit breaker, metrics, security audit, memory write, learning, ledger, consensus, auditor + health + telemetry

### What's Working (LawClaw — Gold Standard)

**Handler boundary (23 systems auto-fire for every command)**
**Capability routing:** Routes unrecognized commands to the correct agent via shared/capabilities.py
**Cross-agent delegation:** /doc -> docuclaw with jurisdiction enrichment, /translate -> interpretclaw -> docuclaw formatting chain
**Self-improvement:** Consensus truth engine, /correct command, source registry (.gov 0.92), truth resolver
**Data pipeline:** Court rules extractor reads 3,800-city jurisdiction files, filing-ready motions
**Document translation:** Legal term preservation (Latin, French, citations, party names)
**All output:** Generated documents export to clawpack_v2/exports/

### What's Partially Connected (17 agents)
Have /delegate routes but no capability routing, no handler boundary, no shared memory:
claw_coder, crustyclaw, dataclaw, designclaw, docuclaw, draftclaw, dreamclaw, flowclaw, interpretclaw, langclaw, liberateclaw, mediclaw, plotclaw, rustypycraw, txclaw, webclaw, llmclaw

### What's Isolated (3 agents)
drawclaw, fileclaw, mathematicaclaw — no cross-agent communication at all.

### Cleanup Completed (May 29, 2026)
**Deleted (15):**
shared/fork/, shared/skills/, shared/search/, shared/batcher.py, shared/latches.py,
shared/patch_ask_llm.py, shared/fix_ask_llm.py, shared/commands.py,
shared/hooks/runners/, agents/lawclaw/law_search/,
scripts/append_validator.py

**Moved (4):**
docuclaw_api.py -> agents/docuclaw/, anthropic_contract.py -> agents/draftclaw/,
edit_tools.py -> agents/drawclaw/, import_scanner.py -> scripts/

**Fixed:**
shared/registry.py — 5 syntax errors repaired (missing commas, stray comma, unclosed dict, duplicate return).
Broken docuclaw delegation path fixed (stale import + wrong function signature).
Now imports cleanly with 16 agents registered via AGENT_REGISTRY.

**Still Broken (known):**
shared/registry.py has 5 agents missing from AGENT_REGISTRY (crustyclaw, designclaw,
liberateclaw, rustypycraw, dreamclaw). Their entries were in unreachable dead code
after the dict closing brace. Need to be merged into the main AGENT_REGISTRY dict.

---

## New Features Deployed (May 29, 2026)

### 1. Capability Registry (shared/capabilities.py)
Maps every capability to its constitutional owner. Every agent handler needs one routing block.
**Deployed to:** LawClaw. **Remaining:** 20 agents.

### 2. Lifecycle Supervisor (shared/lifecycle.py)
Guarantees resource cleanup after every agent invocation. Must be wired into a2a_server.py.

### 3. Memory Staleness (shared/memory_guard.py)
Adds age warnings to facts retrieved from UnifiedMemory.

### 4. Legal Translation Pipeline (lawclaw handler)
/translate command with legal term preservation. Chain: lawclaw -> interpretclaw (translate) -> docuclaw (re-format). Preserves Latin terms, French legal terms, case citations, statutory references, court names, and party names. Stores last document for cross-command reference. All output to exports/.

### 5. 23-System Constitutional Boundary
LawClaw handler boundary activates all 38 shared modules. First agent at 100% utilization.

### 6. PlotClaw Inter-Agent Fixes
All 13 chart commands fixed for cross-agent calling:
- Schema imports changed from relative (`from schema import`) to absolute (`from agents.plotclaw.schema import`)
- Smart title/axis label extraction from natural language input
- Value parsing handles $, K, M, %, comma formats
- Pie chart, bar chart, plot, scatter all confirmed working from lawclaw

---

## Constitutional Violations (Fix Before Building New Features)

### VIOLATION 1: Enforcement Engine Not Activated (Article XI) — CRITICAL
File: a2a_server.py. Wrap process_task() with EnforcementEngine.execute_with_enforcement().

### VIOLATION 2: llmclaw Bypasses Sovereign Gateway (Article I) — CRITICAL
File: agents/llmclaw/agent_handler.py. Route through shared/llm/client.py.

### VIOLATION 3: Guarded Executor Not Wired (Article IV) — CRITICAL
File: a2a_server.py. Wire shared/guarded_executor.py as middleware.

### VIOLATION 4: Three Agents Isolated (Article III) — HIGH
drawclaw, fileclaw, mathematicaclaw. Add call_agent() routes.

### VIOLATION 5: Only LawClaw Uses Shared Memory (Article VI) — HIGH
All 20 non-compliant agent handlers need the 23-system boundary block and _memory.py bridge.

### VIOLATION 6: Registry Missing 5 Agents (Article II) — HIGH
shared/registry.py AGENT_REGISTRY is missing crustyclaw, designclaw, liberateclaw, rustypycraw, dreamclaw. Their entries exist in the file but outside the dict closing brace (unreachable dead code). Merge them into the main dict.

---

## Agent Connectivity Gap Analysis (May 29, 2026)

| Agent | Capability Route | Handler Boundary | Shared Memory | /delegate Route |
|-------|-----------------|-----------------|---------------|-----------------|
| lawclaw | YES | YES | YES | N/A (has /doc, /translate) |
| claw_coder | NO | NO | NO | YES |
| crustyclaw | NO | NO | NO | YES |
| dataclaw | NO | NO | NO | YES |
| designclaw | NO | NO | NO | YES |
| docuclaw | NO | NO | NO | YES |
| draftclaw | NO | NO | NO | YES |
| drawclaw | NO | NO | NO | NO |
| dreamclaw | NO | NO | NO | NO |
| fileclaw | NO | NO | NO | NO |
| flowclaw | NO | NO | NO | YES |
| interpretclaw | NO | NO | NO | NO |
| langclaw | NO | NO | NO | NO |
| liberateclaw | NO | NO | NO | NO |
| llmclaw | NO | NO | NO | NO |
| mathematicaclaw | NO | NO | NO | YES |
| mediclaw | NO | NO | NO | NO |
| plotclaw | NO | NO | NO | NO |
| rustypycraw | NO | NO | NO | NO |
| txclaw | NO | NO | NO | NO |
| webclaw | NO | NO | NO | NO |

20 agents x 3 missing features = 60 total gaps.

---

## Architecture Reference: Claude Code Analysis (May 29, 2026)

The 18-chapter Claude Code architecture was analyzed as a production reference.

| Claude Code Pattern | Clawpack Implementation | Status |
|---------------------|------------------------|--------|
| Agent loop (async generator) | A2A message routing | YES |
| 15-step agent lifecycle with cleanup | shared/lifecycle.py | Built, needs wiring |
| Permission system (7 modes) | shared/enforcement/ | Built, dormant |
| File-based memory with LLM recall | Chronicle SQLite FTS5 + UnifiedMemory | Active |
| Self-describing tools | LawClaw commands | Active |
| Multi-agent orchestration | call_agent() + capability registry | Active |
| Memory staleness | shared/memory_guard.py | Active |

Key insight: Claude Code is monolithic. Clawpack is distributed. Patterns transfer; implementations diverge.

---

## Path Forward (Priority Order)

### Phase 1: Complete New Infrastructure Deployment
1. DONE shared/capabilities.py
2. DONE shared/lifecycle.py
3. DONE shared/memory_guard.py — staleness
4. DONE LawClaw handler — capability routing + 23-system boundary + telemetry + /translate
5. DONE shared/registry.py — fixed syntax errors, docuclaw delegation path
6. Deploy capability routing to remaining 20 agents
7. Wire lifecycle into a2a_server.py

### Phase 2: Constitutional Completion (Tier 1)
1. Wire enforcement/engine.py into a2a_server.py (Article XI)
2. Fix llmclaw's own_llm (Article I)
3. Wire guarded_executor.py into a2a_server.py (Article IV)
4. Wire execution_policy.py

### Phase 3: Legal Cognition (Tier 2)
1. Wire chronicle_helper.py
2. Wire procedural_memory.py
3. Wire three_tier.py

### Phase 4: Multi-Agent Intelligence (Tier 3)
1. Wire smart_router.py
2. Wire agent_router.py

### Phase 5: Operational Polish (Tier 4)
1. validation.py, log_manager.py, shutdown.py, hooks/

### Phase 6: Complete the Mesh
1. Deploy capability routing + handler boundary to all 20 agents
2. Create _memory.py bridge for each agent
3. Fix isolated agents
4. Merge 5 missing agents into registry AGENT_REGISTRY dict

### Phase 7: Boundary Citation Enforcement
Add constitutional postcondition: verify DocuClaw validation block, verify source URLs, warn on incomplete provenance.

---

## LawClaw Is the Constitutional Reference Implementation

**Every agent in Clawpack V2 should model its connectivity after LawClaw.**

When building or modifying any agent:
1. Study agents/lawclaw/agent_handler.py — the 23-system handler boundary + capability routing + /translate chain
2. Study agents/lawclaw/commands/_helpers.py — the shared utility pattern
3. Study agents/lawclaw/commands/_memory.py — the memory bridge pattern
4. Study agents/lawclaw/core/court_rules_extractor.py — the multi-source extraction pattern
5. Every agent MUST have a constitutional handler boundary (23 systems)
6. Every agent MUST have capability routing
7. Every agent MUST write to and read from UnifiedMemory
8. Every agent MUST delegate rather than reimplement

---

## Quick Reference: Files That Matter

| File | Purpose | Status |
|------|---------|--------|
| a2a_server.py | Central message bus, port 8766 | Needs lifecycle + enforcement wiring |
| shared/capabilities.py | Universal command routing | Deploy to all 20 agents |
| shared/registry.py | Agent registration + delegation | Fixed — 16 agents, needs 5 added |
| shared/lifecycle.py | Agent cleanup supervisor | Wire into a2a_server.py |
| shared/memory_guard.py | Confidence + staleness enforcement | Active |
| shared/base_agent.py | Foundation class for all agents | Active |
| shared/_agent_helpers.py | Empire-wide utilities | Active |
| shared/consensus_engine.py | Reputation-based truth scoring | Active |
| shared/source_registry.py | Trust scores for 40+ sources | Active |
| shared/truth_resolver.py | Source conflict resolution | Active |
| shared/decision_ledger.py | Tamper-evident audit chain | Active |
| shared/enforcement/engine.py | Pre/post execution gates | DORMANT — wire into a2a |
| shared/guarded_executor.py | Dangerous ops gateway | DORMANT — wire into a2a |
| shared/procedural_memory.py | Rules and anti-patterns | DORMANT — Tier 2 |
| shared/memory/three_tier.py | Working/semantic/procedural | DORMANT — Tier 2 |
| shared/chronicle_helper.py | Historical self-reference | DORMANT — Tier 2 |
| shared/smart_router.py | Intent-based routing | DORMANT — Tier 3 |
| shared/agent_router.py | Task decomposition | DORMANT — Tier 3 |
| agents/lawclaw/agent_handler.py | Reference implementation | GOLD STANDARD — 100% utilization |
| agents/webclaw/references/lawclaw/jurisdictions/us/ | 3,800+ cities | Active |

---

## Session Log

2026-05-27: All 12 lawclaw commands built. _helpers.py and _memory.py created.

2026-05-28: All 21 agents wired with shared/_agent_helpers.py. 23 commands memory-wired.
Constitutional Command Lifecycle section added. First cross-agent flow proven.

2026-05-29 (morning): Constitutional execution boundary activated. Consensus engine deployed.
/correct command for self-healing. Court rules extractor built. /doc generates jurisdiction-specific
documents. Source registry fixed (.gov 0.92, .us courts 0.85). Truth resolver patched.

2026-05-29 (afternoon): Inter-agent mesh testing. PlotClaw schema imports fixed across all 13 chart
commands (from schema -> from agents.plotclaw.schema). Smart title/axis label extraction added.
Value parsing handles $, K, M, %, comma formats. Pie, bar, plot, scatter commands confirmed
working from lawclaw. Capability registry routing verified (/bar, /pie, /plot all route to plotclaw).
Registry syntax errors discovered and fixed — 5 bugs including missing commas, stray comma,
unclosed dict, duplicate return statement. Docuclaw delegation path repaired (stale import
from shared.docuclaw_api changed to agents.docuclaw.docuclaw_api, function signature
corrected from create_for_agent to create_document).

**Infrastructure deployed:**
- Capability registry (shared/capabilities.py) — universal command routing
- Lifecycle supervisor (shared/lifecycle.py) — guaranteed cleanup
- Memory staleness — age warnings on facts
- 23-system constitutional boundary — LawClaw at 100% shared infrastructure utilization
- /translate command — legal translation with term preservation (Latin, French, citations, party names)
- Translation pipeline: lawclaw -> interpretclaw (translate) -> docuclaw (re-format) -> lawclaw
- _last_document storage for cross-command document reference
- All generated documents export to clawpack_v2/exports/
- PlotClaw inter-agent chart generation from any agent
- Agent Registry (shared/registry.py) — 16 agents registered, delegation layer active

**Cleanup completed:**
- 15 dead files/folders deleted (fork/, skills/, search/, batcher.py, latches.py,
  patch_ask_llm.py, fix_ask_llm.py, commands.py, hooks/runners/, law_search/,
  append_validator.py)
- 4 misplaced files moved to correct agent directories
- shared/registry.py repaired (was silently broken since creation)
- shared/commands.py deleted (dead code, no imports)

**Architecture analysis:**
- Claude Code 18-chapter reference analyzed
- Clawpack patterns validated against production system
- Key differences documented (monolithic vs distributed)

**Constitutional doctrine established:**
- Citation attribution: WebClaw owns sources, DocuClaw reflects citations, Boundary enforces completeness
- /doc is constitutional — domain enrichment before delegation, not document generation
- Capability registry preserves Article II — agents recognize foreign capabilities and delegate
- /translate is constitutional — legal domain enrichment (term preservation) before delegation

**Known gaps:**
- 5 agents missing from AGENT_REGISTRY (crustyclaw, designclaw, liberateclaw, rustypycraw, dreamclaw)
- 20 agents lack capability routing + handler boundary + shared memory
- 3 agents isolated (drawclaw, fileclaw, mathematicaclaw)
- Enforcement engine dormant (Article XI)
- Guarded executor not wired (Article IV)
- llmclaw bypasses Sovereign Gateway (Article I)

**Current utilization:** LawClaw at 100% of shared infrastructure (38/38 files).
**Total commands:** 25. **Constitutional runtime:** ACTIVE.
