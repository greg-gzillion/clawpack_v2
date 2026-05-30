# CLAWPACK V2 — Architecture & Design

## What Is Clawpack V2?

A sovereign AI agent ecosystem. 21 specialized agents sharing a common knowledge database (Chronicle 448MB SQLite FTS5), governed by a Constitution, communicating through an A2A protocol with circuit breaker protection and task state tracking. No agent works alone. No agent talks to an LLM directly. All knowledge belongs to all agents.

## Constitutional Foundation

`shared/CONSTITUTION_v1.md` is the supreme law. Key principles:

- **Article I — Sovereignty**: All LLM access through Sovereign Gateway only. No agent imports LLM libraries.
- **Article II — Separation of Powers**: Each agent has one domain. No crossing.
- **Article III — Delegation**: Before expanding an agent, delegate to an existing specialist.
- **Article V — Truth Hierarchy**: `web_verified > chronicle > memory > inference`. Lower truth NEVER overrides higher.
- **Article VI — Shared Memory**: Knowledge learned by one agent belongs to all. One memory. One empire.

## Three-Layer Architecture

### Layer 1: A2A Server (`a2a_server.py`, port 8766)
Central message bus. Every agent registers here. Every inter-agent communication routes through A2A.
- `GET /health` — Server status + memory stats
- `GET /v1/agents` — List all 21 agents
- `POST /v1/message/{agent}` — Send task to any agent

### Layer 2: Shared Infrastructure (`shared/`)
Every agent inherits 36 systems through the constitutional boundary block:

| Tier | Systems | Purpose |
|------|---------|---------|
| **Tier 1 — Constitutional Closure** | lifecycle, enforcement/engine, guarded_executor, execution_policy | Execution safety |
| **Tier 2 — Cognition** | chronicle_helper, procedural_memory, three_tier | Knowledge retrieval |
| **Tier 3 — Intelligence** | smart_router, agent_router | Task routing |
| **Tier 4 — Operational** | validation, log_manager, shutdown, hooks | Operations |
| **Tier 5 — Governance** | budget, rate_limiter, error_handler, metrics, security | Resource protection |
| **Tier 6 — Memory & Truth** | memory_guard, source_registry, truth_resolver, decision_ledger, consensus_engine, auditor | Knowledge integrity |
| **Tier 7 — Infrastructure** | input_handler, permissions, registry, jurisdiction_validator, enforcement/gates, config, constitutional_command, court_rules_schema, decomposer, output_handler, router, compactor | System services |
| **Tier 8 — Telemetry** | observability, chronicle_ledger | Monitoring |

**BaseAgent** (`shared/base_agent.py`) provides:
- `call_agent()` — cross-agent calls with circuit breaker + task state tracking
- `ask_llm()` — Sovereign Gateway access (4 providers, 17 models)
- `cached_search()` — web search with automatic DataClaw caching (24hr TTL)
- `lookup_jurisdiction()` — library/hospital/police/building codes from 3,800+ cities via Chronicle FTS5
- `search_chronicle()` — 448MB SQLite FTS5 full-text search
- `learn()` / `recall()` — cross-agent memory persistence

### Layer 3: 21 Specialized Agents (`agents/`)

| # | Agent | Domain | Key Capabilities | Status |
|---|-------|--------|-----------------|--------|
| 1 | **lawclaw** | Law Research & Analysis | 24 commands, /doc enrichment, /translate chain, 3,800-city civic database | ✅ 10/10 |
| 2 | **claw_coder** | Code Generation | 39 languages, memory recall before generation, code validation | ✅ 10/10 |
| 3 | **crustyclaw** | Rust AI | Audit/pinch/fix, standalone binary fallback | ✅ 10/10 |
| 4 | **mediclaw** | Medical Analysis | Hospital geolocation, urgency triage, /doc, professional/layperson detection | ✅ 10/10 |
| 5 | **designclaw** | Graphic Design | Brand identity, building code lookup from jurisdiction files | ✅ 10/10 |
| 6 | **draftclaw** | Technical Drawings | Blueprints, CAD, structural, permit compliance, design criteria | ✅ 10/10 |
| 7 | **dreamclaw** | AI Vision | /dream, /imagine, context-gathered generation | ✅ 10/10 |
| 8 | **interpretclaw** | Translation | 42 languages (incl. Latin, ASL), cross-platform TTS, Braille (opt-in) | ✅ 10/10 |
| 9 | **langclaw** | Language Teaching | Lessons, vocab, practice, cross-platform TTS | ✅ 10/10 |
| 10 | **liberateclaw** | Model Liberation | Obliterated model management, 17 models | ✅ 10/10 |
| 11 | **dataclaw** | Data Processing | 41K local files, Chronicle writes, search cache | ✅ 10/10 |
| 12 | **docuclaw** | Document Creation | 31 commands, validation engine, multi-format export | ⚠️ 9/10 |
| 13 | **flowclaw** | Diagrams & Flowcharts | Mermaid.js, browser rendering, specialized LLM adapter | ⚠️ 9/10 |
| 14 | **plotclaw** | Charts & Graphs | 15 chart types, smart title/axis extraction | ⚠️ 8/10 |
| 15 | **mathematicaclaw** | Math & Computation | SymPy + Plotly, 9 commands | ⚠️ 8/10 |
| 16 | **webclaw** | Web Search & Indexing | Chronicle owner, 3,800+ city references, 35K+ entries | ⚠️ 8/10 |
| 17 | **llmclaw** | Model Management | Sovereign Gateway orchestration, 4 providers | ⚠️ 8/10 |
| 18 | **fileclaw** | File Operations | 41+ formats, universal file handler | ⚠️ 8/10 |
| 19 | **txclaw** | Blockchain | TX operations, smart contracts | ⚠️ 8/10 |
| 20 | **rustypycraw** | Code Crawler | AST crawling, delegates to claw_coder + crustyclaw | ⚠️ 8/10 |
| 21 | **drawclaw** | AI Drawing & Art | 15 commands, library resource lookup | ⚠️ 8/10 |

## Data Flow: How an Agent Answers a Query
User: "mediclaw> /diagnose chest pain in Denver CO"
↓
A2A Server → agent_handler.py → handle()
↓
Command: diagnose.py run(args, agent=self)
↓

_memory.recall("chest pain Denver") — check prior cases

agent.search_chronicle("chest pain Denver") — 448MB FTS5

agent.ask_llm(prompt) → Sovereign Gateway → Ollama/Anthropic/Groq

lookup_hospitals("Denver CO") → Chronicle FTS5 jurisdiction search

_memory.remember() — persist for future
↓
36-system boundary fires (lifecycle, enforcement, metrics, etc.)
↓
Response returned with diagnosis + nearest hospitals + authoritative sources

text

## Cross-Agent Communication

All agents communicate through three paths:
1. **Capability Registry** — unrecognized commands auto-route to correct agent
2. **Direct Delegation** — `/delegate plotclaw /bar Q1 45 Q2 62`
3. **Enriched Delegation** — domain expertise added before forwarding

Every cross-agent call is:
- **Circuit breaker protected** (5 failures = 60s open circuit)
- **Task state tracked** (pending → running → completed/failed/killed)
- **Search cached** (24hr TTL via DataClaw, zero tokens on repeat queries)

## The Chronicle — Shared Knowledge Database

`data/chronicle.db` — SQLite FTS5, 448MB, 35,000+ interactions.

Contains indexed full-text of all reference files from `webclaw/references/`:
- **lawclaw**: 3,800+ city jurisdictions (courts, police, jails, hospitals, libraries, building permits)
- **mediclaw**: 91 medical specialties
- **txclaw**: 60+ blockchain documentation categories
- **claw_coder**: 39 programming language references
- **All other agents**: Design, language, math references

Every agent queries the same Chronicle. No per-agent databases. No duplicated data.

## LLM Provider Chain

The Sovereign Gateway manages 4 providers with automatic fallback:

| Provider | Model | Priority | Type |
|----------|-------|----------|------|
| Ollama | deepseek-r1:8b | 1 | Local, free |
| OpenRouter | gemma-4-26b | 2 | Free tier |
| Anthropic | claude-haiku-4-5 | 3 | Cloud |
| Groq | llama-3.3-70b-versatile | 4 | Cloud |

## File Organization
clawpack_v2/
├── a2a_server.py # Central message bus (port 8766)
├── clawpack.py # Interactive menu
├── shared/ # 36 shared systems
│ ├── base_agent.py # Foundation class (circuit breaker, task state, jurisdiction lookup)
│ ├── task_state.py # Task state machine (pending→running→completed/failed/killed)
│ ├── search_cache.py # DataClaw-based search cache (24hr TTL)
│ ├── capabilities.py # Universal command routing
│ └── ... # 32 more systems
├── agents/ # 21 specialized agents
│ ├── webclaw/ # Chronicle owner, web search, 3,800+ city references
│ ├── dataclaw/ # Local data + search cache
│ ├── lawclaw/ # Gold standard reference implementation
│ ├── mediclaw/ # Hospital geolocation + medical AI
│ └── ... # 17 more agents
├── data/
│ ├── chronicle.db # 448MB SQLite FTS5
│ └── task_store.json # Cross-agent task tracking
├── models/ # LLM configurations
└── scripts/ # Testing, auditing, debugging


