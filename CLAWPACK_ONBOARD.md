# CLAWPACK V2 - AI ONBOARDING CONTEXT

## What This Is
21-agent AI ecosystem. Menu-driven CLI. A2A routing on port 8766.
448MB Chronicle SQLite index at data/chronicle.db. Constitutional governance.
Built by Greg.

## Before You Write Any Code
1. Ask to see the current file if modifying an existing command.
2. Ask to see a working command if building a new stub.
3. Do not assume file contents - they may differ from conversation history.
4. State what you are about to do before doing it. One function at a time.

## How Commands Load
Commands in each agent's commands/ directory are loaded dynamically.
Each file needs: name = "/commandname" and def run(args, agent=None): at module level.
No manual registration - just drop the .py file in the directory.
Critical: The handler's if/elif chain must explicitly import and call the command.
If missing from the chain, falls to else -> _gather_context() -> webclaw -> LLM (45-90s).

## Constitution (NON-NEGOTIABLE)
- All LLM access goes to Sovereign Gateway only (shared/llm/client.py). No direct API calls.
- All exceptions must log. except: pass is UNCONSTITUTIONAL.
- Truth hierarchy: web_verified > chronicle > memory > inference.
- Every agent has defined jurisdiction. No crossing.

---

## Current State - May 30, 2026

### Runtime Health
| Metric | Value |
|--------|-------|
| Agent availability | 21/21 responsive |
| Median /help latency | 0.2s |
| A2A transport | Healthy (port 8766) |
| Chronicle index | 35,553 interactions |
| LLM providers | 4/4 operational |
| Provider chain | Groq -> Ollama -> OpenRouter -> Anthropic |
| Lifecycle cleanup errors | 0 (contract drift resolved May 30) |
| Civic commands | Chronicle FTS5 direct (0.03-0.28s) |

### Agent Constitutional Status
Constitutional = has call_agent() boundary + get_capable_agent() routing + _memory bridge.

| Status | Count | Agents |
|--------|-------|--------|
| Constitutional | 13 | lawclaw, claw_coder, crustyclaw, dataclaw, designclaw, drawclaw, dreamclaw, flowclaw, interpretclaw, langclaw, liberateclaw, mediclaw, draftclaw |
| Partial (no routing) | 7 | docuclaw, llmclaw, mathematicaclaw, plotclaw, rustypycraw, txclaw, webclaw |
| Needs upgrade | 1 | fileclaw |

### Provider Chain (Sovereign Gateway)
| Priority | Provider | Model | Latency | Cost |
|----------|----------|-------|---------|------|
| 1 | Groq | llama-3.3-70b-versatile | 0.7s | Free |
| 2 | Ollama | deepseek-r1:8b | 0.8s | Free (local) |
| 3 | OpenRouter | google/gemma-4-26b-a4b-it:free | 0.7s | Free tier |
| 4 | Anthropic | claude-haiku-4-5-20251001 | 1.2s | Paid |

Provider order: shared/llm/providers/__init__.py detect_providers()
Active model: models/active_model.json
Switch at runtime: llmclaw> /use groq or /use deepseek-r1:8b

---

## Resolved This Session (May 30, 2026)

### Lifecycle Contract Drift - ALL FIXED
Three errors fired on every agent invocation, now eliminated:
- cannot import name 'log_event' -> replaced with get_chronicle().record_fetch()
- DecisionLedger.record() unexpected keyword 'action' -> migrated to record_action()
- ChronicleLedger.record_fetch() unexpected keyword 'agent' -> corrected kwargs
Result: 0 lifecycle cleanup errors across all 21 agents.

### Civic Commands - Now Chronicle FTS5 Direct
/detention, /police, /library, /hospital were missing from handler dispatch chain.
Fell to else -> _gather_context() -> webclaw -> LLM (45-90s).
Added to if/elif with direct Chronicle FTS5 import. Now 0.03-0.28s.

### Provider Order Fixed
base_agent.py ask_llm() had provider='anthropic' hardcoded.
Removed. Gateway now respects detect_providers() order (Groq first).

### Dreamclaw Timeout Fixed
_handler() called _gather_context() BEFORE /help check.
Restructured: /help and /stats return immediately. Was >20s, now 0.2s.

### Model Fixes
- OpenRouter: z-ai/glm-5.1 -> google/gemma-4-26b-a4b-it:free
- Ollama: hardcoded qwen3-coder:30b -> reads deepseek-r1:8b from active_model.json
- Timeouts: Groq 60->90s, call_sync total 120->300s

---

## Known Active Work (Not Blocking)
| Area | Scope | Impact |
|------|-------|--------|
| Chronicle recover_by_context | 19 call sites, 8 modules | Non-blocking warnings |
| Capability routing | 7 partial agents | No auto-routing |
| Shared memory | fileclaw | No memory bridge |
| Enforcement engine | Dormant | Violations voluntary |
| Guarded executor | Dormant | Ops bypass review |
| Registry | 5 agents outside dict | Can't delegate via registry |

---

## Pattern for Upgrading Any Agent (3 files)
1. commands/_memory.py - copy from lawclaw, change agent name
2. commands/_helpers.py - agent-specific utilities + jurisdiction lookup
3. agent_handler.py - add boundary block, capability routing, _gather_context()

Minimum constitutional else block:
    else:
        from shared.capabilities import get_capable_agent
        target = get_capable_agent(cmd, "agentname")
        if target:
            result = self.call_agent(target, task, timeout=60)
        elif args:
            result = self.ask_llm(...)
        else:
            result = "Type /help for commands"

---

## Quick Reference: Files That Matter
| File | Purpose | Status |
|------|---------|--------|
| a2a_server.py | Central message bus, port 8766 | Active |
| shared/llm/client.py | Sovereign Gateway | Active |
| shared/llm/providers/__init__.py | Provider detection + chain | Active |
| shared/capabilities.py | Universal command routing | Active |
| shared/registry.py | Agent registration | 16/21 |
| shared/lifecycle.py | Agent cleanup supervisor | Active (0 errors) |
| shared/base_agent.py | Foundation class | Active |
| shared/_agent_helpers.py | Empire-wide utilities | Active |
| shared/decision_ledger.py | Audit chain | Active |
| shared/consensus_engine.py | Truth scoring | Active |
| shared/source_registry.py | Trust scores | Active |
| shared/truth_resolver.py | Conflict resolution | Active |
| shared/memory_guard.py | Staleness enforcement | Active |
| shared/enforcement/engine.py | Execution gates | Dormant |
| shared/guarded_executor.py | Dangerous ops gateway | Dormant |
| agents/lawclaw/agent_handler.py | Reference implementation | Gold standard |
| agents/webclaw/references/lawclaw/jurisdictions/us/ | 3,800+ cities | Active |
| models/active_model.json | Active model config | Active |
| data/chronicle.db | 448MB SQLite FTS5 | Active |

---

## Session Log

2026-05-27: All 12 lawclaw commands built. _helpers.py and _memory.py created.

2026-05-28: All 21 agents wired with shared/_agent_helpers.py. First cross-agent flow.

2026-05-29: Constitutional boundary activated. Consensus engine deployed.
Capability registry + lifecycle supervisor + memory staleness deployed.
PlotClaw schema imports fixed (13 commands). Registry syntax repaired (5 bugs).
Docuclaw delegation path fixed. /translate pipeline built. 15 dead files deleted.
Task state machine + search cache deployed. 8 agent READMEs created.
Groq model: llama-3.1-8b -> llama-3.3-70b-versatile.

2026-05-30: RUNTIME STABILIZATION.
- Civic commands: Chronicle FTS5 direct (0.03-0.28s, was 45-90s).
- Provider order: Groq primary (was Anthropic hardcoded).
- Lifecycle contract drift: RESOLVED. 0 cleanup errors, all 21 agents.
- Dreamclaw: /help 0.2s (was >20s timeout).
- OpenRouter: google/gemma-4-26b-a4b-it:free (was broken).
- Ollama: synced to active_model.json (was hardcoded).
- All 21 agents tested: 21/21 responsive, median /help 0.2s.
- All 4 LLM providers tested: all operational.
- README rewritten: benchmark data, known work, execution flow diagram.
