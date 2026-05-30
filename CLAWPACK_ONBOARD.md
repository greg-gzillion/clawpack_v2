# CLAWPACK V2 - AI ONBOARDING CONTEXT

## What This Is
21-agent AI ecosystem. Menu-driven CLI. A2A routing on port 8766.
448MB Chronicle SQLite index at data/chronicle.db. Constitutional governance.
Built by Greg.

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
| Status | Count | Agents |
|--------|-------|--------|
| Constitutional (boundary + routing + memory) | 13 | lawclaw, claw_coder, crustyclaw, dataclaw, designclaw, drawclaw, dreamclaw, flowclaw, interpretclaw, langclaw, liberateclaw, mediclaw, draftclaw |
| Partial (no capability routing) | 7 | docuclaw, llmclaw, mathematicaclaw, plotclaw, rustypycraw, txclaw, webclaw |
| Needs upgrade | 1 | fileclaw |

### Resolved This Session (May 30)
- Lifecycle contract drift: log_event, record(action=), record_fetch(agent=) all fixed. 0 cleanup errors.
- Civic commands (/detention /police /library /hospital): now direct Chronicle FTS5. Was 45-90s via LLM.
- Provider order: Groq primary (was Anthropic hardcoded in base_agent.py ask_llm).
- Dreamclaw /help: 0.2s (was >20s timeout). Skips _gather_context() and 23-system boundary.
- OpenRouter model: google/gemma-4-26b-a4b-it:free (was broken z-ai/glm-5.1).
- Ollama model: reads from active_model.json (was hardcoded qwen3-coder:30b).
- Timeouts: Groq 60->90s, call_sync total 120->300s.
- README: rewritten with benchmark data, known work section, execution flow diagram.

### Known Active Work
| Area | Scope |
|------|-------|
| Chronicle recover_by_context signature | 19 call sites, non-blocking warnings |
| Capability routing | 7 partial agents need get_capable_agent() |
| Shared memory | fileclaw has no memory bridge |
| Enforcement engine | Dormant, needs a2a_server.py wiring |
| Guarded executor | Dormant, needs a2a_server.py wiring |
| Registry | 5 agents outside AGENT_REGISTRY dict |

---

## Constitution (NON-NEGOTIABLE)
- All LLM access goes to Sovereign Gateway only (shared/llm/client.py). No direct API calls.
- All exceptions must log. except: pass is UNCONSTITUTIONAL.
- Truth hierarchy: web_verified > chronicle > memory > inference.
- Every agent has defined jurisdiction. No crossing.

## Before You Write Any Code
1. Ask to see the current file if modifying an existing command.
2. Ask to see a working command if building a new stub.
3. Do not assume file contents - they may differ from conversation history.
4. State what you are about to do before doing it. One function at a time.

## How Commands Load
Commands in each agent's commands/ directory are loaded dynamically.
Each file needs: name = "/commandname" and def run(args, agent=None): at module level.
No manual registration - just drop the .py file in the directory.
The handler's if/elif chain must include the command or it falls to the else block.

## Pattern for Upgrading Any Agent
1. commands/_memory.py - copy from lawclaw, change agent name
2. commands/_helpers.py - agent-specific utilities + jurisdiction lookup
3. agent_handler.py - add boundary block, capability routing, _gather_context()

## Provider Chain (Sovereign Gateway)
| Priority | Provider | Model | Latency |
|----------|----------|-------|---------|
| 1 | Groq | llama-3.3-70b-versatile | 0.7s |
| 2 | Ollama | deepseek-r1:8b | 0.8s |
| 3 | OpenRouter | google/gemma-4-26b-a4b-it:free | 0.7s |
| 4 | Anthropic | claude-haiku-4-5-20251001 | 1.2s |

## Quick Reference: Files That Matter
| File | Purpose | Status |
|------|---------|--------|
| a2a_server.py | Central message bus, port 8766 | Active |
| shared/llm/client.py | Sovereign Gateway | Active |
| shared/llm/providers/__init__.py | Provider detection + chain order | Active |
| shared/capabilities.py | Universal command routing | Active |
| shared/registry.py | Agent registration + delegation | 16/21 registered |
| shared/lifecycle.py | Agent cleanup supervisor | Active, 0 errors |
| shared/base_agent.py | Foundation class for all agents | Active |
| shared/_agent_helpers.py | Empire-wide utilities | Active |
| shared/decision_ledger.py | Tamper-evident audit chain | Active |
| shared/consensus_engine.py | Reputation-based truth scoring | Active |
| shared/source_registry.py | Trust scores for 40+ sources | Active |
| shared/truth_resolver.py | Source conflict resolution | Active |
| shared/memory_guard.py | Confidence + staleness enforcement | Active |
| shared/enforcement/engine.py | Pre/post execution gates | Dormant |
| shared/guarded_executor.py | Dangerous ops gateway | Dormant |
| agents/lawclaw/agent_handler.py | Reference implementation | Gold standard |
| agents/webclaw/references/lawclaw/jurisdictions/us/ | 3,800+ cities | Active |
| models/active_model.json | Active model + provider config | Active |
| data/chronicle.db | 448MB SQLite FTS5 index | Active |
