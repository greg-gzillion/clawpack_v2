# CLAWPACK V2 — Architecture & Design

## What Is Clawpack V2?

A sovereign AI agent ecosystem. 21 specialized agents sharing a common knowledge database (Chronicle), governed by a Constitution, communicating through an A2A protocol. No agent works alone. No agent talks to an LLM directly. All knowledge belongs to all agents.

## Constitutional Foundation

`shared/CONSTITUTION_v1.md` is the supreme law. Key principles:

- **Article I — Sovereignty**: All LLM access through `shared/llm/client.py` only. No agent imports LLM libraries.
- **Article II — Separation of Powers**: Each agent has one domain. No agent accumulates powers from multiple ministries.
- **Article III — Delegation**: Before expanding an agent, delegate to an existing specialist.
- **Article V — Truth Hierarchy**: `web_verified > chronicle > memory > inference`. Lower truth NEVER overrides higher.
- **Article VI — Shared Memory**: Knowledge learned by one agent belongs to all. One memory. One empire.

## Three-Layer Architecture

### Layer 1: A2A Server (`a2a_server.py`, port 8766)
Central message bus. Every agent registers here. Every inter-agent communication routes through A2A.
- `GET /health` — Server status + memory stats
- `GET /v1/agents` — List all 21 agents
- `POST /v1/message/{agent}` — Send task to any agent
- `GET /v1/data/building-codes` — Query jurisdiction data

### Layer 2: Shared Ministries (`shared/`)
Every agent inherits these:

| Ministry | Path | Purpose |
|----------|------|---------|
| Sovereign Gateway | `shared/llm/client.py` | ALL model access. 4 providers, 25 models. Budget, audit, fallback. |
| Judiciary | `shared/enforcement/` | 19 forbidden patterns. Pre/post execution gates. |
| Unified Memory | `shared/memory/` | Chronicle-backed. Cross-agent recall. |
| BaseAgent | `shared/base_agent.py` | Foundation class. `search_chronicle()`, `ask_llm()`, `call_agent()` |
| Truth Resolver | `shared/truth_resolver.py` | Enforces `web_verified > chronicle > memory > inference` |
| Decision Ledger | `shared/decision_ledger.py` | Tamper-evident hash chain. Verifiable audit. |
| Guarded Executor | `shared/guarded_executor.py` | Only legal path for dangerous operations. |
| Memory Guard | `shared/memory_guard.py` | Inference never persists. Confidence > 0.75 threshold. |
| Import Scanner | `shared/import_scanner.py` | Detects forbidden LLM imports. |

### Layer 3: 21 Specialized Agents (`agents/`)
Each agent has:
- `agent_handler.py` — A2A interface (how other agents call it)
- `commands/` — CLI command implementations
- `core/` — Engine/logic
- `providers/` — Data access (WebClaw, APIs)
- References live in `webclaw/references/` (single canonical copy)

## Agent Directory

| # | Agent | Domain | Delegates To | Status |
|---|-------|--------|-------------|--------|
| 1 | lawclaw | Law Research & Analysis | DocuClaw, WebClaw | ✅ |
| 2 | flowclaw | Flowcharts & Diagrams | DocuClaw | ✅ |
| 3 | docuclaw | Document Creation | — | ✅ |
| 4 | mathematicaclaw | Math & Computation | DocuClaw, PlotClaw | ✅ |
| 5 | liberateclaw | Model Liberation | Sovereign Gateway | ✅ |
| 6 | txclaw | TX Blockchain | DocuClaw, FileClaw | ⚠️ |
| 7 | interpretclaw | Translation & Speech | WebClaw | ✅ |
| 8 | langclaw | Language Teaching | WebClaw | ✅ |
| 9 | claw_coder | Code (39 languages) | DocuClaw | ✅ |
| 10 | dataclaw | Data Processing | FileClaw | ❌ |
| 11 | webclaw | Web Search & Indexing | Chronicle | ✅ |
| 12 | fileclaw | Files (52 formats) | DocuClaw | ✅ |
| 13 | plotclaw | Charts & Graphs | DocuClaw | ✅ |
| 14 | mediclaw | Medical Analysis | DocuClaw, WebClaw | ✅ |
| 15 | dreamclaw | AI Vision | Sov. Gateway | ✅ |
| 16 | designclaw | Graphic Design | DocuClaw | ✅ |
| 17 | draftclaw | Technical Drawings | DocuClaw | ✅ |
| 18 | crustyclaw | Rust AI | ClawCoder | ✅ |
| 19 | rustypycraw | Code Crawler | FileClaw | ✅ |
| 20 | drawclaw | AI Drawing & Art | DocuClaw | ✅ |
| 21 | llmclaw | Model Manager | Sov. Gateway | ✅ |

## Data Flow: How an Agent Answers a Query
User: "mediclaw> /diagnose chest pain"
↓
A2A Server → agent_handler.py → MedicalEngine._search_context()
↓
chronicle.recover_by_context("chest pain", limit=100)
↓
SQLite FTS5 searches 76,463 indexed entries
↓
Returns medical references + jurisdiction hospital data
↓
MedicalEngine._call_llm(context + prompt)
↓
Sovereign Gateway → Anthropic API (or Ollama fallback)
↓
LLM synthesizes with citations from Chronicle
↓
Response returned to user with sources

text

## The Chronicle — Shared Knowledge Database

`data/chronicle.db` — SQLite FTS5, 448MB, ~76,463 entries.

Contains indexed full-text of all reference files from `webclaw/references/`:
- **lawclaw**: 70+ legal categories + 50-state jurisdictions (courts, police, jails, hospitals, libraries, building permits)
- **mediclaw**: 91 medical specialties
- **txclaw**: 60+ blockchain documentation categories
- **claw_coder**: 39 programming language references
- **All other agents**: Design, language, math references

Every agent queries the same Chronicle. No per-agent databases. No duplicated data.

## Modularity

Each agent is small. MedicLaw is 2 Python files + modules. LangClaw is ~15 files. The heavy data (references) lives in `webclaw/references/` — indexed once, shared by all.

Agents don't import each other. They communicate through A2A messages. An agent calls another agent by name:
```python
self.call_agent("webclaw", "search medical journals", timeout=15)
LLM Provider Chain
The Sovereign Gateway (shared/llm/client.py) manages 4 providers with automatic fallback:

Anthropic (claude-haiku) — primary

Groq (llama-3.1-8b-instant) — fallback

OpenRouter (gemma-4-26b) — free tier

Ollama (local) — 17 models, always available

Direct Model (obliterated) — 5 models, sovereign, no API

File Organization
text
clawpack_v2/
├── a2a_server.py          # Central message bus
├── clawpack.py            # Interactive menu
├── shared/                # Universal ministries (all agents inherit)
│   ├── base_agent.py      # Foundation class
│   ├── CONSTITUTION_v1.md # Supreme law
│   ├── llm/               # Sovereign Gateway
│   ├── enforcement/       # Judiciary
│   └── memory/            # Unified knowledge
├── agents/                # 21 specialized agents
│   ├── webclaw/           # Web search + reference indexing
│   │   └── references/    # ALL reference data (single canonical copy)
│   ├── lawclaw/           # Law research
│   ├── mediclaw/          # Medical analysis
│   └── ...                # 18 more agents
├── data/
│   └── chronicle.db       # Shared knowledge database (76K entries)
├── models/                # LLM configurations + obliterated models
└── scripts/               # Indexing, testing, debugging tools
