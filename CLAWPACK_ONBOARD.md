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

---

## Current State — May 29, 2026

### What's Working (LawClaw — Gold Standard)
LawClaw is the constitutional reference implementation. All other agents should follow its pattern.

**Handler boundary (13 systems auto-fire for every command):**
1. Budget check (shared/llm/budget.py)
2. Rate limit (shared/rate_limiter.py)
3. Circuit breaker (shared/error_handler.py)
4. Metrics (shared/metrics.py)
5. Security audit (shared/security.py)
6. Memory write (unified_memory.py)
7. Learning (shared/_agent_helpers.py)
8. Ledger (shared/decision_ledger.py)
9. Consensus (shared/consensus_engine.py)
10. Auditor (shared/llm/auditor.py)
11. Budget record (shared/llm/budget.py)
12. Health check (shared/observability.py)
13. Telemetry (chronicle_ledger.py)

**Capability routing:**
LawClaw can route unrecognized commands to the correct agent via `shared/capabilities.py`.
User types `/plot bar sales` in lawclaw → silently routes to plotclaw.
No per-agent command duplication. Article II preserved.

**Cross-agent delegation:**
- `/doc` → docuclaw with jurisdiction context + live court rules
- `remember_court()` / `recall_court()` handoff between `/jurisdiction` and `/doc`
- `call_agent("webclaw")` for context gathering

**Self-improvement:**
- Consensus truth engine with structured claim extraction
- `/correct` command for community corrections
- Source registry: .gov at 0.92, .us courts at 0.85
- Truth resolver: .gov wildcard returns web_verified

**Data pipeline:**
- Court rules extractor reads 3,800-city files
- Location extraction handles structured args
- Filing-ready motions with correct state rules

### What's Partially Connected (17 agents)
These agents have `/delegate` routes but no capability routing, no handler boundary, no shared memory:
claw_coder, crustyclaw, dataclaw, designclaw, docuclaw, draftclaw, dreamclaw, flowclaw, interpretclaw, langclaw, liberateclaw, mediclaw, plotclaw, rustypycraw, txclaw, webclaw, llmclaw

### What's Isolated (3 agents)
drawclaw, fileclaw, mathematicaclaw — no cross-agent communication at all.

### What's Dormant (Built but Not Wired)
- Enforcement engine (shared/enforcement/engine.py) — pre/post execution gates exist but never called
- Guarded executor (shared/guarded_executor.py) — dangerous ops gateway exists but never called
- Procedural memory (shared/memory/procedural_memory.py) — rules and patterns exist but never called
- Three-tier memory (shared/memory/three_tier.py) — exists but never called
- Hooks system (shared/hooks/) — types exist, runners are Claude Code-specific (can be cut)

---

## New Features to Connect (May 29, 2026)

### 1. Capability Registry (`shared/capabilities.py`) — NEW, MUST DEPLOY
Maps every capability (/plot, /code, /translate, etc.) to its constitutional owner.
Every agent handler needs one routing block added to enable universal commands.

**To add to any agent handler:**
```python
# In handle(), replace the final else: block with:
            else:
                # Constitutional capability routing
                from shared.capabilities import get_capable_agent
                target = get_capable_agent(cmd, self.name)
                if target:
                    result = self.call_agent(target, task, timeout=60)
                elif args:
                    # Fallback: ask LLM with context
                    context = self._gather_context(args)
                    result = self.ask_llm(f"Query: {args}\n\nContext:\n{context}")
                else:
                    result = "Type /help for commands"
Agents that still need this: All 20 except lawclaw.

2. Lifecycle Cleanup (shared/lifecycle.py) — NEW, MUST DEPLOY
Guarantees resource cleanup after every agent invocation.
Must be wired into a2a_server.py around process_task() calls.

3. Memory Staleness (shared/memory_guard.py update) — NEW
Adds age warnings to facts retrieved from UnifiedMemory.
Prevents old facts from being treated as current truth.

4. Handler Boundary — Must Copy to All Agents
The 13-system constitutional boundary from lawclaw's handler.
Every agent needs this. Change agent name from "lawclaw" to the agent's name.

Constitutional Violations (Fix Before Building New Features)
VIOLATION 1: Enforcement Engine Not Activated (Article XI)
Severity: CRITICAL. File: a2a_server.py
Wrap process_task() with EnforcementEngine.execute_with_enforcement().

VIOLATION 2: llmclaw Bypasses Sovereign Gateway (Article I)
Severity: CRITICAL. File: agents/llmclaw/agent_handler.py
llmclaw has own_llm=True. Must route through shared/llm/client.py.

VIOLATION 3: Guarded Executor Not Wired (Article IV)
Severity: CRITICAL. File: a2a_server.py
Wire shared/guarded_executor.py as middleware.

VIOLATION 4: Three Agents Isolated (Article III)
Severity: HIGH. Files: drawclaw, fileclaw, mathematicaclaw agent_handlers
Add call_agent() routes. Minimum: delegate to docuclaw for export.

VIOLATION 5: Only LawClaw Uses Shared Memory (Article VI)
Severity: HIGH. All 20 non-compliant agent handlers
Add the 13-system boundary block. Create _memory.py bridge for each agent.

What to Clean Up (Dead Code)
Safe to Delete Now:
shared/fork/ — Claude Code-specific fork system, not applicable

shared/skills/ — Claude Code slash-command system, not applicable

shared/hooks/runners/ — Claude Code-specific implementations (keep types)

shared/search/ — bitmap index for file search, not needed

shared/batcher.py — tool call batching, commands are sequential

shared/latches.py — cache preservation, Claude Code-specific

shared/patch_ask_llm.py — legacy patch

shared/fix_ask_llm.py — legacy patch

shared/commands.py — 12 lines, dead code

shared/docuclaw_api.py — belongs in docuclaw, not shared

shared/anthropic_contract.py — belongs in draftclaw, not shared

shared/import_scanner.py — dev tool, move to scripts/

shared/edit_tools.py — image editing, belongs in drawclaw

shared/input_handler.py — CLI-specific, belongs in clawpack.py

shared/output_handler.py — CLI-specific, belongs in clawpack.py

Keep but Don't Wire Yet (Future-Proofing):
shared/compactor.py — context compression, needed when payloads grow

shared/decomposer.py — task decomposition, needed for complex /doc requests

shared/procedural_memory.py — rules/patterns, needed for anti-pattern learning

shared/three_tier.py — working/semantic/procedural memory, future memory architecture

Path Forward (Priority Order)
Phase 1: Deploy New Infrastructure (THIS SESSION)
✅ shared/capabilities.py — saved

✅ shared/lifecycle.py — saved

✅ shared/memory_guard.py — staleness added

✅ LawClaw handler updated with capability routing + telemetry

⬜ Deploy capability routing to remaining 20 agents

⬜ Wire lifecycle into a2a_server.py

Phase 2: Close Constitutional Violations (NEXT SESSION)
Activate enforcement engine in a2a_server.py

Fix llmclaw's own_llm

Wire guarded executor

Phase 3: Complete the Mesh (FOLLOWING SESSIONS)
Add capability routing + handler boundary to all agents

Create _memory.py bridge for each agent

Fix isolated agents (drawclaw, fileclaw, mathematicaclaw)

Phase 4: Clean Up
Delete dead modules (safe list above)

Move misplaced modules to correct locations

Re-run constitutional compliance audit

LawClaw Is the Constitutional Reference Implementation
Every agent in Clawpack V2 should model its connectivity after LawClaw.

When building or modifying any agent:

Study agents/lawclaw/agent_handler.py — the handler boundary + capability routing pattern

Study agents/lawclaw/commands/_helpers.py — the shared utility pattern

Study agents/lawclaw/commands/_memory.py — the memory bridge pattern

Study agents/lawclaw/core/court_rules_extractor.py — the multi-source extraction pattern

Every agent MUST have a constitutional handler boundary (13 systems)

Every agent MUST have capability routing (one block, delegates unknown commands)

Every agent MUST write to and read from UnifiedMemory

Every agent MUST delegate rather than reimplement

Quick Reference: Files That Matter
File	Purpose	Status
a2a_server.py	Central message bus, port 8766	Needs lifecycle + enforcement wiring
shared/capabilities.py	Universal command routing	NEW — deploy to all agents
shared/lifecycle.py	Agent cleanup supervisor	NEW — wire into a2a_server.py
shared/memory_guard.py	Confidence + staleness enforcement	Updated with staleness
shared/base_agent.py	Foundation class for all agents	Active
shared/_agent_helpers.py	Empire-wide utilities	Active
shared/consensus_engine.py	Reputation-based truth scoring	Active
shared/source_registry.py	Trust scores for 40+ sources	Active
shared/truth_resolver.py	Source conflict resolution	Active
shared/decision_ledger.py	Tamper-evident audit chain	Active
shared/enforcement/engine.py	Pre/post execution gates	DORMANT — wire into a2a
shared/guarded_executor.py	Dangerous ops gateway	DORMANT — wire into a2a
agents/lawclaw/agent_handler.py	Reference implementation	GOLD STANDARD
agents/webclaw/references/lawclaw/jurisdictions/us/	3,800+ cities	Active
Session Log
2026-05-27: All 12 lawclaw commands built. _helpers.py and _memory.py created.

2026-05-28: All 21 agents wired with shared/_agent_helpers.py. 23 commands memory-wired.
Constitutional Command Lifecycle section added. First cross-agent flow proven.

2026-05-29: Constitutional execution boundary activated (13 systems). Consensus engine deployed.
/correct command for self-healing. Court rules extractor built. /doc generates jurisdiction-specific
documents. Source registry fixed (.gov 0.92, .us courts 0.85). Truth resolver patched.

Capability registry deployed — universal command routing across all agents.
Lifecycle supervisor deployed — guaranteed cleanup for every agent invocation.
Memory staleness added — facts now carry age warnings.
LawClaw handler updated — capability routing + telemetry active.
Claude Code architecture reference — 18-chapter production system analysis completed.
Patterns validated: generator loop, file-based memory, self-describing tools, fork agents for
cache sharing, hooks over plugins. Clawpack's distributed implementation matches proven patterns.