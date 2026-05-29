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
1. DocuClaw's validation block is present (`Constitutional Source Validation`)
2. Source URLs are included (`https://` in output)
3. If either is missing, a constitutional warning is appended

No new subsystem needed. The ministries already exist. The boundary enforces their cooperation.

---

## Current State — May 29, 2026

### LawClaw Utilization of Shared Infrastructure: 15 of 38 files (39%)

**Actively Connected (15):**
`base_agent.py`, `_agent_helpers.py`, `capabilities.py`, `consensus_engine.py`, `source_registry.py`, `truth_resolver.py`, `decision_ledger.py`, `memory_guard.py`, `rate_limiter.py`, `error_handler.py`, `security.py`, `metrics.py`, `observability.py`, `llm/budget.py`, `llm/auditor.py`

**Dormant — Constitutional Completion (4 files, Tier 1 priority):**
`lifecycle.py`, `enforcement/engine.py`, `guarded_executor.py`, `execution_policy.py`

**Dormant — Legal Cognition (3 files, Tier 2 priority):**
`chronicle_helper.py`, `procedural_memory.py`, `three_tier.py`

**Dormant — Multi-Agent Intelligence (2 files, Tier 3 priority):**
`smart_router.py`, `agent_router.py`

**Dormant — Operational Polish (remaining files, Tier 4 priority):**
`validation.py`, `log_manager.py`, `shutdown.py`, `hooks/`, `config.py`, `registry.py`, `a2a_client.py`, `files/`, `compactor.py`, `decomposer.py`

LawClaw today is a functioning legal research agent — capable of answering questions with citations.
After Tier 1: constitutionally complete — every action validated, every resource cleaned up.
After Tier 2: learns from experience — remembers what worked, avoids what failed.
After Tier 3: orchestrates the federation — decomposes complex tasks across 21 agents.

### What's Working (LawClaw — Gold Standard)

**Handler boundary (13 systems auto-fire for every command):**
Budget check, Rate limit, Circuit breaker, Metrics, Security audit, Memory write, Learning, Ledger, Consensus, Auditor, Budget record, Health check, Telemetry

**Capability routing:**
LawClaw can route unrecognized commands to the correct agent via `shared/capabilities.py`.
User types `/plot bar sales` in lawclaw → silently routes to plotclaw. Article II preserved.

**Cross-agent delegation:**
- `/doc` → docuclaw with jurisdiction context + live court rules
- `/doc` is a specialized lawclaw command that enriches with legal domain expertise before delegating. This is constitutional — not a violation of Article II. Other agents access document generation through the capability registry for simple delegation, or build their own enriched versions for domain-specific handoffs.
- `remember_court()` / `recall_court()` handoff between `/jurisdiction` and `/doc`

**Self-improvement:**
- Consensus truth engine with structured claim extraction
- `/correct` command for community corrections
- Source registry: .gov at 0.92, .us courts at 0.85
- Truth resolver: .gov wildcard returns web_verified

**Data pipeline:**
- Court rules extractor reads 3,800-city jurisdiction files
- Filing-ready motions with correct state rules (FL 1.140(b)(6), NV 12(b)(6))

### What's Partially Connected (17 agents)
Have `/delegate` routes but no capability routing, no handler boundary, no shared memory:
claw_coder, crustyclaw, dataclaw, designclaw, docuclaw, draftclaw, dreamclaw, flowclaw, interpretclaw, langclaw, liberateclaw, mediclaw, plotclaw, rustypycraw, txclaw, webclaw, llmclaw

### What's Isolated (3 agents)
drawclaw, fileclaw, mathematicaclaw — no cross-agent communication at all.

### Cleanup Completed (May 29, 2026)
**Deleted (11):** `shared/fork/`, `shared/skills/`, `shared/search/`, `shared/batcher.py`, `shared/latches.py`, `shared/patch_ask_llm.py`, `shared/fix_ask_llm.py`, `shared/commands.py`, `shared/hooks/runners/`, `agents/lawclaw/law_search/`

**Moved (4):** `docuclaw_api.py` → `agents/docuclaw/`, `anthropic_contract.py` → `agents/draftclaw/`, `edit_tools.py` → `agents/drawclaw/`, `import_scanner.py` → `scripts/`

---

## New Features Deployed (May 29, 2026)

### 1. Capability Registry (`shared/capabilities.py`)
Maps every capability to its constitutional owner. Every agent handler needs one routing block.
**Deployed to:** LawClaw. **Remaining:** 20 agents.

### 2. Lifecycle Supervisor (`shared/lifecycle.py`)
Guarantees resource cleanup after every agent invocation. Must be wired into `a2a_server.py`.

### 3. Memory Staleness (`shared/memory_guard.py`)
Adds age warnings to facts retrieved from UnifiedMemory.

---

## Constitutional Violations (Fix Before Building New Features)

### VIOLATION 1: Enforcement Engine Not Activated (Article XI) — CRITICAL
File: `a2a_server.py`. Wrap `process_task()` with `EnforcementEngine.execute_with_enforcement()`.

### VIOLATION 2: llmclaw Bypasses Sovereign Gateway (Article I) — CRITICAL
File: `agents/llmclaw/agent_handler.py`. Route through `shared/llm/client.py`.

### VIOLATION 3: Guarded Executor Not Wired (Article IV) — CRITICAL
File: `a2a_server.py`. Wire `shared/guarded_executor.py` as middleware.

### VIOLATION 4: Three Agents Isolated (Article III) — HIGH
drawclaw, fileclaw, mathematicaclaw. Add `call_agent()` routes.

### VIOLATION 5: Only LawClaw Uses Shared Memory (Article VI) — HIGH
All 20 non-compliant agent handlers need the 13-system boundary block and `_memory.py` bridge.

---

## Agent Connectivity Gap Analysis (May 29, 2026)

| Agent | Capability Route | Handler Boundary | Shared Memory | /delegate Route |
|-------|-----------------|-----------------|---------------|-----------------|
| lawclaw | ✅ | ✅ | ✅ | N/A (has /doc) |
| claw_coder | ❌ | ❌ | ❌ | ✅ |
| crustyclaw | ❌ | ❌ | ❌ | ✅ |
| dataclaw | ❌ | ❌ | ❌ | ✅ |
| designclaw | ❌ | ❌ | ❌ | ✅ |
| docuclaw | ❌ | ❌ | ❌ | ✅ |
| draftclaw | ❌ | ❌ | ❌ | ✅ |
| drawclaw | ❌ | ❌ | ❌ | ❌ |
| dreamclaw | ❌ | ❌ | ❌ | ❌ |
| fileclaw | ❌ | ❌ | ❌ | ❌ |
| flowclaw | ❌ | ❌ | ❌ | ✅ |
| interpretclaw | ❌ | ❌ | ❌ | ❌ |
| langclaw | ❌ | ❌ | ❌ | ❌ |
| liberateclaw | ❌ | ❌ | ❌ | ❌ |
| llmclaw | ❌ | ❌ | ❌ | ❌ |
| mathematicaclaw | ❌ | ❌ | ❌ | ✅ |
| mediclaw | ❌ | ❌ | ❌ | ❌ |
| plotclaw | ❌ | ❌ | ❌ | ❌ |
| rustypycraw | ❌ | ❌ | ❌ | ❌ |
| txclaw | ❌ | ❌ | ❌ | ❌ |
| webclaw | ❌ | ❌ | ❌ | ❌ |

**20 agents × 3 missing features = 60 total gaps.**

---

## Architecture Reference: Claude Code Analysis (May 29, 2026)

The 18-chapter Claude Code architecture was analyzed as a production reference. Clawpack's distributed implementation matches proven patterns:

| Claude Code Pattern | Clawpack Implementation | Status |
|---------------------|------------------------|--------|
| Agent loop (async generator) | A2A message routing | ✅ Different architecture, same concept |
| 15-step agent lifecycle with cleanup | `shared/lifecycle.py` | ✅ Built, needs wiring |
| Permission system (7 modes) | `shared/enforcement/` | ❌ Built, dormant |
| File-based memory with LLM recall | Chronicle SQLite FTS5 + UnifiedMemory | ✅ Active |
| Self-describing tools | LawClaw commands | ✅ Active |
| Fork agents for cache sharing | Not applicable | N/A — different architecture |
| Hooks over plugins | `shared/hooks/` (types only) | ⚠️ Types kept, runners cut |
| Bitmap pre-filters for search | Not applicable | N/A — no file search problem |
| Sticky latches for cache preservation | Not applicable | N/A — different architecture |
| Multi-agent orchestration | `call_agent()` + capability registry | ✅ Active |
| Memory staleness | `shared/memory_guard.py` | ✅ Newly added |

**Key insight:** Claude Code is a monolithic TypeScript process. Clawpack is a distributed federation of 21 Python agents communicating via A2A. The patterns transfer; the implementations diverge where the architectures demand it. Do not copy Claude Code patterns that assume a single process with shared memory.

---

## Path Forward (Priority Order)

### Phase 1: Complete New Infrastructure Deployment
1. ✅ `shared/capabilities.py` — saved
2. ✅ `shared/lifecycle.py` — saved
3. ✅ `shared/memory_guard.py` — staleness added
4. ✅ LawClaw handler updated with capability routing + telemetry
5. ⬜ Deploy capability routing to remaining 20 agents (one block each, ~2 hours)
6. ⬜ Wire lifecycle into `a2a_server.py` (~5 minutes)

### Phase 2: Constitutional Completion (Tier 1 — closes critical violations)
1. Wire `enforcement/engine.py` into `a2a_server.py` (closes Article XI)
2. Fix llmclaw's `own_llm` (closes Article I)
3. Wire `guarded_executor.py` into `a2a_server.py` (closes Article IV)
4. Wire `execution_policy.py`

### Phase 3: Legal Cognition (Tier 2 — makes LawClaw a learning practitioner)
1. Wire `chronicle_helper.py` — historical self-reference
2. Wire `procedural_memory.py` — retain successful patterns, learn from failures
3. Wire `three_tier.py` — working + semantic + procedural memory

### Phase 4: Multi-Agent Intelligence (Tier 3 — unlocks federation)
1. Wire `smart_router.py` — intent-based delegation
2. Wire `agent_router.py` — task decomposition across agents

### Phase 5: Operational Polish (Tier 4)
1. `validation.py`, `log_manager.py`, `shutdown.py`, `hooks/`

### Phase 6: Complete the Mesh
1. Deploy capability routing + handler boundary to all 20 agents
2. Create `_memory.py` bridge for each agent
3. Fix isolated agents (drawclaw, fileclaw, mathematicaclaw)

### Phase 7: Boundary Citation Enforcement
Add constitutional postcondition to the handler boundary:
- Verify DocuClaw validation block present
- Verify source URLs included
- Warn on incomplete provenance

---

## LawClaw Is the Constitutional Reference Implementation

**Every agent in Clawpack V2 should model its connectivity after LawClaw.**

When building or modifying any agent:
1. Study `agents/lawclaw/agent_handler.py` — the handler boundary + capability routing pattern
2. Study `agents/lawclaw/commands/_helpers.py` — the shared utility pattern
3. Study `agents/lawclaw/commands/_memory.py` — the memory bridge pattern
4. Study `agents/lawclaw/core/court_rules_extractor.py` — the multi-source extraction pattern
5. Every agent MUST have a constitutional handler boundary (13 systems)
6. Every agent MUST have capability routing (one block, delegates unknown commands)
7. Every agent MUST write to and read from UnifiedMemory
8. Every agent MUST delegate rather than reimplement

---

## Quick Reference: Files That Matter

| File | Purpose | Status |
|------|---------|--------|
| `a2a_server.py` | Central message bus, port 8766 | Needs lifecycle + enforcement wiring |
| `shared/capabilities.py` | Universal command routing | Deploy to all 20 agents |
| `shared/lifecycle.py` | Agent cleanup supervisor | Wire into a2a_server.py |
| `shared/memory_guard.py` | Confidence + staleness enforcement | Active |
| `shared/base_agent.py` | Foundation class for all agents | Active |
| `shared/_agent_helpers.py` | Empire-wide utilities | Active |
| `shared/consensus_engine.py` | Reputation-based truth scoring | Active |
| `shared/source_registry.py` | Trust scores for 40+ sources | Active |
| `shared/truth_resolver.py` | Source conflict resolution | Active |
| `shared/decision_ledger.py` | Tamper-evident audit chain | Active |
| `shared/enforcement/engine.py` | Pre/post execution gates | DORMANT — wire into a2a |
| `shared/guarded_executor.py` | Dangerous ops gateway | DORMANT — wire into a2a |
| `shared/procedural_memory.py` | Rules and anti-patterns | DORMANT — Tier 2 |
| `shared/memory/three_tier.py` | Working/semantic/procedural | DORMANT — Tier 2 |
| `shared/chronicle_helper.py` | Historical self-reference | DORMANT — Tier 2 |
| `shared/smart_router.py` | Intent-based routing | DORMANT — Tier 3 |
| `shared/agent_router.py` | Task decomposition | DORMANT — Tier 3 |
| `agents/lawclaw/agent_handler.py` | Reference implementation | GOLD STANDARD |
| `agents/webclaw/references/lawclaw/jurisdictions/us/` | 3,800+ cities | Active |

---

## Session Log

2026-05-27: All 12 lawclaw commands built. _helpers.py and _memory.py created.

2026-05-28: All 21 agents wired with shared/_agent_helpers.py. 23 commands memory-wired.
Constitutional Command Lifecycle section added. First cross-agent flow proven.

2026-05-29: Constitutional execution boundary activated (13 systems). Consensus engine deployed.
/correct command for self-healing. Court rules extractor built. /doc generates jurisdiction-specific
documents. Source registry fixed (.gov 0.92, .us courts 0.85). Truth resolver patched.

**Infrastructure deployed:**
- Capability registry (`shared/capabilities.py`) — universal command routing
- Lifecycle supervisor (`shared/lifecycle.py`) — guaranteed cleanup
- Memory staleness — age warnings on facts
- LawClaw handler updated — capability routing + 13-system boundary + telemetry

**Cleanup completed:**
- 11 dead files/folders deleted from shared/
- 4 misplaced files moved to correct agent directories
- 2 legacy law_search files removed
- Hook runners deleted, types preserved

**Architecture analysis:**
- Claude Code 18-chapter reference analyzed
- Clawpack patterns validated against production system
- Key differences documented (monolithic vs distributed)

**Constitutional doctrine established:**
- Citation attribution: WebClaw owns sources, DocuClaw reflects citations, Boundary enforces completeness
- /doc is constitutional — domain enrichment before delegation, not document generation
- Capability registry preserves Article II — agents recognize foreign capabilities and delegate

**Current utilization:** LawClaw at 39% of shared infrastructure (15/38 files).
**Path to completion:** 4 Tiers documented with specific files and priorities.
**Total commands:** 24. **Constitutional runtime:** ACTIVE.