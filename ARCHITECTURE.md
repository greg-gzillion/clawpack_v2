# CLAWPACK V2 - Architecture & Design

## What Is Clawpack V2?

A policy-enforced local-first multi-agent runtime. 21 specialized agents sharing a common knowledge database (Chronicle 448MB SQLite FTS5), governed by a Constitution, communicating through an A2A protocol with circuit breaker protection. No agent works alone. No agent talks to an LLM directly. Execution passes through enforced policy gates before agent dispatch.

## Constitutional Foundation

`shared/CONSTITUTION_v1.md` is the supreme law. Key principles:

- **Article I - Sovereignty**: All LLM access through Sovereign Gateway only (shared/llm/client.py). No agent imports LLM libraries directly.
- **Article II - Separation of Powers**: Each agent has one domain. No crossing.
- **Article III - Delegation**: Before expanding an agent, delegate to an existing specialist.
- **Article V - Truth Hierarchy**: `web_verified > chronicle > memory > inference`. Lower truth NEVER overrides higher.
- **Article VI - Shared Memory**: Knowledge learned by one agent belongs to all.

## Three-Layer Architecture

### Layer 1: A2A Server (`a2a_server.py`, port 8766)
Central message bus. Every agent registers here. Every inter-agent communication routes through A2A.
- `GET /health` - Server status + memory stats
- `GET /v1/agents` - List all 21 agents
- `POST /v1/message/{agent}` - Send task to any agent
- Lifecycle cleanup fires on every request (0 errors as of May 30)

### Layer 2: Shared Infrastructure (`shared/`)
36+ shared systems organized in 8 tiers:

| Tier | Systems | Purpose |
|------|---------|---------|
| Constitutional Closure | lifecycle, enforcement/engine, guarded_executor, execution_policy | Execution safety |
| Cognition | chronicle_helper, procedural_memory, three_tier | Knowledge retrieval |
| Intelligence | smart_router, agent_router | Task routing |
| Operational | validation, log_manager, shutdown, hooks | Operations |
| Governance | budget, rate_limiter, error_handler, metrics, security | Resource protection |
| Memory & Truth | memory_guard, source_registry, truth_resolver, decision_ledger, consensus_engine, auditor | Knowledge integrity |
| Infrastructure | input_handler, permissions, registry, jurisdiction_validator, enforcement/gates, config, constitutional_command, court_rules_schema, decomposer, output_handler, router, compactor | System services |
| Telemetry | observability, chronicle_ledger | Monitoring |
| Accessibility | accessibility.py (unified), speech.py, locale.py | Voice, TTS, STT, Braille, translation |

**BaseAgent** (`shared/base_agent.py`) provides:
- `call_agent()` - cross-agent calls with circuit breaker + task state tracking
- `ask_llm()` - Sovereign Gateway access (4 providers)
- `lookup_jurisdiction()` - library/hospital/police/building codes from 3,800+ cities via Chronicle FTS5 (0.03-0.28s)
- `search_chronicle()` - 448MB SQLite FTS5 full-text search
- `learn()` / `recall()` - cross-agent memory persistence

### Layer 3: 21 Specialized Agents (`agents/`)

| # | Agent | Domain | Status |
|---|-------|--------|--------|
| 1 | lawclaw | Law Research & Analysis - 24 commands, /doc enrichment, /translate chain | Constitutional |
| 2 | claw_coder | Code Generation - 39 languages, code validation | Constitutional |
| 3 | crustyclaw | Rust AI - Audit/pinch/fix | Constitutional |
| 4 | mediclaw | Medical Analysis - Hospital geolocation, urgency triage | Constitutional |
| 5 | designclaw | Graphic Design - Building code lookup | Constitutional |
| 6 | draftclaw | Technical Drawings - Blueprints, CAD, structural | Constitutional |
| 7 | dreamclaw | AI Vision - /dream, /imagine, 0.2s /help | Constitutional |
| 8 | interpretclaw | Translation - 42 languages | Constitutional |
| 9 | langclaw | Language Teaching - Lessons, vocab, practice | Constitutional |
| 10 | liberateclaw | Model Liberation - Obliterated model management | Constitutional |
| 11 | dataclaw | Data Processing - 41K local files, Chronicle writes | Constitutional |
| 12 | drawclaw | AI Drawing & Art - 15 commands | Constitutional |
| 13 | flowclaw | Diagrams & Flowcharts - Mermaid.js, browser rendering | Constitutional |
| 14 | docuclaw | Document Creation - 31 commands, multi-format export | Partial |
| 15 | llmclaw | Model Management - Sovereign Gateway orchestration | Partial |
| 16 | mathematicaclaw | Math & Computation - SymPy + Plotly, 9 commands | Partial |
| 17 | plotclaw | Charts & Graphs - 15 chart types | Partial |
| 18 | rustypycraw | Code Crawler - AST crawling | Partial |
| 19 | txclaw | Blockchain - TX operations, smart contracts | Partial |
| 20 | webclaw | Web Search & Indexing - Chronicle owner, 35K+ entries | Partial |
| 21 | fileclaw | File Operations - 41+ formats | Needs upgrade |

Constitutional = call_agent() boundary + get_capable_agent() routing + _memory bridge.
Partial = missing capability routing. 13 constitutional, 7 partial, 1 needs upgrade.

## Data Flow: How an Agent Answers a Query

User: "mediclaw> /diagnose chest pain in Denver CO"
|
v
A2A Server -> agent_handler.py -> handle()
|
v
Command: diagnose.py run(args, agent=self)
|
+-- _memory.recall("chest pain Denver") [check prior cases]
+-- agent.search_chronicle("chest pain") [448MB FTS5]
+-- agent.lookup_jurisdiction("Denver CO") [Chronicle FTS5, 0.03s]
+-- agent.ask_llm(prompt) [Sovereign Gateway]
+-- _memory.remember() [persist for future]
|
v
Lifecycle cleanup fires (0 errors)
|
v
Response: diagnosis + nearest hospitals + authoritative sources

text

## Cross-Agent Communication

All agents communicate through three paths:
1. **Capability Registry** - unrecognized commands auto-route to correct agent via shared/capabilities.py
2. **Direct Delegation** - call_agent() with circuit breaker protection
3. **Enriched Delegation** - domain expertise added before forwarding (e.g., lawclaw -> docuclaw with court context)

Every cross-agent call is:
- **Circuit breaker protected** (5 consecutive failures = 60s open circuit)
- **Budget enforced** (daily limit via Sovereign Gateway)

## The Chronicle - Shared Knowledge Database

`data/chronicle.db` - SQLite FTS5, 448MB, 35,553 interactions.

Contains indexed full-text of all reference files:
- **lawclaw**: 3,800+ city jurisdictions (courts, police, jails, hospitals, libraries, building permits)
- **mediclaw**: 91 medical specialties
- **claw_coder**: 39 programming language references
- **All other agents**: Design, language, math, blockchain references

Every agent queries the same Chronicle. No per-agent databases. Civic commands (/detention, /police, /library, /hospital, /jurisdiction) return directly from Chronicle FTS5 in 0.03-0.28s with zero LLM calls.

## LLM Provider Chain (Sovereign Gateway)

| Priority | Provider | Model | Latency | Cost |
|----------|----------|-------|---------|------|
| 1 | Groq | llama-3.3-70b-versatile | 0.7s | Free |
| 2 | Ollama | model from active_model.json (currently gemma3:4b) | 0.8-30s | Free (local) |
| 3 | OpenRouter | google/gemma-4-26b-a4b-it:free | 0.7s | Free tier |
| 4 | Anthropic | claude-haiku-4-5-20251001 | 1.2s | Paid |

Provider order: shared/llm/providers/__init__.py detect_providers()
Active model: models/active_model.json
Switch at runtime: llmclaw> /use groq or /use deepseek-r1:8b

## File Organization
clawpack_v2/
a2a_server.py Central message bus (port 8766)
clawpack.py Interactive menu
shared/ 36 shared systems
llm/client.py Sovereign Gateway
llm/providers/ Provider detection + chain order
base_agent.py Foundation class
capabilities.py Universal command routing
lifecycle.py Agent cleanup supervisor (0 errors)
event_bus.py Canonical event bus for all system input
registry.py Agent registration (16/21)
enforcement/engine.py Execution gates (active - pre-execution gate on every A2A request)
guarded_executor.py Dangerous ops gateway (wired, dormant pending activation)
agents/ 21 specialized agents
lawclaw/ Gold standard reference implementation
webclaw/ Chronicle owner, 3,800+ city references
mediclaw/ Hospital geolocation + medical AI
... 18 more agents
data/
chronicle.db 448MB SQLite FTS5
models/
active_model.json Active model + provider config
