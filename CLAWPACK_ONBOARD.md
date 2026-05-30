# CLAWPACK V2 — AI ONBOARDING CONTEXT

## What This Is
21-agent AI ecosystem. Menu-driven CLI. A2A routing on port 8766.
448MB Chronicle SQLite index at data/chronicle.db. Constitutional governance.
Built by Greg.

## Current State — May 30, 2026

### Runtime Health
| Metric | Value |
|--------|-------|
| Agent availability | 21/21 responsive |
| Median /help latency | 0.2s |
| A2A transport | Healthy (port 8766) |
| Chronicle index | 35,553 interactions |
| LLM providers | 4/4 operational (Groq, Ollama, OpenRouter, Anthropic) |
| Lifecycle cleanup errors | 0 (contract drift resolved) |
| Civic commands | Chronicle FTS5 direct (0.03-0.28s) |

### Agent Constitutional Status

| Status | Count | Agents |
|--------|-------|--------|
| Constitutional | 13 | lawclaw, claw_coder, crustyclaw, dataclaw, designclaw, drawclaw, dreamclaw, flowclaw, interpretclaw, langclaw, liberateclaw, mediclaw, draftclaw |
| Partial (no capability routing) | 7 | docuclaw, llmclaw, mathematicaclaw, plotclaw, rustypycraw, txclaw, webclaw |
| Needs upgrade | 1 | fileclaw |

### Provider Chain (Sovereign Gateway)
| Priority | Provider | Model | Latency | Status |
|----------|----------|-------|---------|--------|
| 1 | Groq | llama-3.3-70b-versatile | 0.7s | Free, rate-limited on large prompts |
| 2 | Ollama | deepseek-r1:8b | 0.8s | Local, unlimited |
| 3 | OpenRouter | google/gemma-4-26b-a4b-it:free | 0.7s | Free tier, intermittent rate limits |
| 4 | Anthropic | claude-haiku-4-5-20251001 | 1.2s | Paid, reliable |

### Resolved (May 30, 2026)
- Lifecycle contract drift: log_event, record(action=), record_fetch(agent=) all fixed — 0 cleanup errors
- Civic commands: /detention /police /library /hospital now direct Chronicle FTS5 — was 45-90s via LLM
- Provider order: Groq primary (was Anthropic hardcoded in base_agent.py)
- Dreamclaw timeout: /help 0.2s (was >20s)
- OpenRouter model: google/gemma-4-26b-a4b-it:free (was broken z-ai/glm-5.1)

### Known Active Work
| Area | Scope |
|------|-------|
| Chronicle recover_by_context signature normalization | 19 call sites, non-blocking warnings |
| Capability routing deployment | 7 partial agents need get_capable_agent() |
| Shared memory adoption | 1 agent (fileclaw) has no memory bridge |
| Enforcement engine wiring | Dormant, needs a2a_server.py integration |
| Guarded executor activation | Dormant, needs a2a_server.py integration |
| Registry completeness | 5 agents outside AGENT_REGISTRY dict |

---

## Constitution (NON-NEGOTIABLE)
- All LLM access goes to Sovereign Gateway only (shared/llm/client.py). No direct API calls.
- All exceptions must log. except: pass is UNCONSTITUTIONAL.
- Truth hierarchy: web_verified > chronicle > memory > inference.
- Every agent has defined jurisdiction. No crossing.

## Before You Write Any Code
1. Ask to see the current file if modifying an existing command.
2. Ask to see a working command if building a new stub.
3. Do not assume file contents — they may differ from conversation history.
4. State what you are about to do before doing it. One function at a time.

## How Commands Load
Commands in each agent's commands/ directory are loaded dynamically.
Each file needs: name = "/commandname" and def run(args, agent=None): at module level.
No manual registration — just drop the .py file in the directory.
The handler's if/elif chain must include the command or it falls to the else block.

## Pattern for Upgrading Any Agent (3 files, 5 minutes)
1. commands/_memory.py — copy from lawclaw, change agent name
2. commands/_helpers.py — agent-specific utilities + jurisdiction lookup
3. agent_handler.py — add import time, _gather_context(), boundary block, capability routing

## Quick Reference: Files That Matter
| File | Purpose | Status |
|------|---------|--------|
| a2a_server.py | Central message bus, port 8766 | Active |
| shared/llm/client.py | Sovereign Gateway | Active — Groq primary |
| shared/llm/providers/__init__.py | Provider detection + chain order | Active |
| shared/capabilities.py | Universal command routing | Active |
| shared/registry.py | Agent registration + delegation | 16/21 registered |
| shared/lifecycle.py | Agent cleanup supervisor | Active — 0 errors |
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
