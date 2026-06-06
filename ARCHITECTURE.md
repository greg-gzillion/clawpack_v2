# CLAWPACK V2 - Architecture & Design

## What Is Clawpack V2?

A policy-enforced local-first multi-agent runtime. 21 specialized agents sharing
a common knowledge database (Chronicle 448MB SQLite FTS5), governed by a Constitution,
communicating through an A2A protocol with circuit breaker protection. BM25 retrieval
with source confidence scoring. DataClaw cache for local-first knowledge retention.

## Constitutional Foundation

`shared/CONSTITUTION_v1.md` is the supreme law. Key principles:

- **Article I - Sovereignty**: All LLM access through Sovereign Gateway only (shared/llm/client.py).
- **Article II - Separation of Powers**: Each agent has one domain. No crossing.
- **Article III - Delegation**: Before expanding an agent, delegate to an existing specialist.
- **Article V - Truth Hierarchy**: `web_verified > chronicle > memory > inference`.
- **Article VI - Shared Memory**: Knowledge learned by one agent belongs to all.
- **Article VII - No Silent Failures**: All exceptions must log. `except: pass` is UNCONSTITUTIONAL.

## Three-Layer Architecture

### Layer 1: A2A Server (`a2a_server.py`, port 8766)
Central message bus. Every agent registers here. All inter-agent communication routes through A2A.
- `GET /health` - Server status + memory stats
- `GET /v1/agents` - List all 21 agents
- `POST /v1/message/{agent}` - Send task to any agent
- Circuit breaker: 5 consecutive failures = 60s open circuit
- Sovereignty enforcement: 6 patterns blocked at HTTP boundary (403)

### Layer 2: Shared Infrastructure (`shared/`)
85 shared modules (44 connected, 41 dormant). Key systems:

| Tier | Key Systems | Purpose |
|------|-------------|---------|
| Retrieval | search_cache, base_agent (cached_search) | Cache-first retrieval |
| Constitutional | lifecycle, enforcement, guarded_executor | Execution safety |
| Intelligence | smart_router, agent_router | Task routing |
| Governance | budget, rate_limiter, error_handler, metrics | Resource protection |
| Memory | memory_guard, source_registry, truth_resolver | Knowledge integrity |
| Accessibility | accessibility.py, speech.py, locale.py | Voice, TTS, STT, Braille |

**BaseAgent** (`shared/base_agent.py`) provides:
- `call_agent()` - cross-agent calls with circuit breaker
- `ask_llm()` - Sovereign Gateway access (4 providers)
- `cached_search()` - cache-first retrieval with WebClaw BM25 fallback
- `search_chronicle()` - 448MB SQLite FTS5 full-text search
- `get_cached_result()` / `cache_result()` - DataClaw cache operations

### Layer 3: 21 Specialized Agents (`agents/`)

| # | Agent | Domain | Status |
|---|-------|--------|--------|
| 1 | lawclaw | Legal Research - 33 commands, 3,800-city civic database | Active |
| 2 | claw_coder | Code Generation - 39 languages | Active |
| 3 | crustyclaw | Rust AI - Audit/pinch/fix | Active |
| 4 | mediclaw | Medical Analysis - 91 specialties, hospital geolocation | Active |
| 5 | designclaw | Graphic Design | Active |
| 6 | draftclaw | Technical Drawings - Blueprints, CAD | Active |
| 7 | dreamclaw | AI Vision | Active |
| 8 | interpretclaw | Translation - 42 languages | Active |
| 9 | langclaw | Language Teaching | Active |
| 10 | liberateclaw | Model Liberation | Active |
| 11 | dataclaw | Data Processing + Cache Storage | Active |
| 12 | drawclaw | AI Drawing & Art | Active |
| 13 | flowclaw | Diagrams & Flowcharts | Active |
| 14 | docuclaw | Document Creation - 31 commands | Active |
| 15 | llmclaw | Model Management - Sovereign Gateway | Active |
| 16 | mathematicaclaw | Math & Computation | Active |
| 17 | plotclaw | Charts & Graphs - 15 chart types | Active |
| 18 | rustypycraw | Code Crawler | Active |
| 19 | txclaw | TX.org Blockchain - 135 live URLs + 529 local files | Active |
| 20 | webclaw | Web Search + BM25 Retrieval - Chronicle owner | Active |
| 21 | fileclaw | File Operations - 41+ formats | Active |

Validation: 21/21 agents pass (June 5, 2026).

## Retrieval Architecture

```
User Query -> Agent Handler -> _gather_context() -> cached_search()
  -> DataClaw Cache (agents/dataclaw/cache/{agent}/)
  -> (miss) WebClaw BM25 -> Chronicle FTS5 (runtime/chronicle.db, 448MB)
  -> final_score = bm25_score * source_weight
  -> Context -> ask_llm() -> Response
```

### Two Agent Classes
- **BM25 agents (9)**: Return raw retrieval with score/source/dedup markers
- **Non-search agents (12)**: Route through ask_llm(), markers stripped
- Both paths WORK — different output format

## DataClaw — Cache + Local Storage

- `agents/dataclaw/cache/{agent}/` — WebClaw result cache, 24hr TTL, JSON
- `agents/dataclaw/references/{agent}/` — 21 agent directories for local data
- `shared/search_cache.py` — cache engine (get_cached, cache_search, get_cache_stats)
- Only lawclaw actively populating cache. Target: all retrieval agents.

## The Chronicle - Shared Knowledge Database

`runtime/chronicle.db` - SQLite FTS5, 448MB, 35,000+ interactions.

Contains indexed full-text of all reference files:
- **lawclaw**: 3,800+ city jurisdictions (courts, police, jails, hospitals, libraries)
- **mediclaw**: 91 medical specialties
- **txclaw**: TX.org blockchain documentation (529 local + 135 live URLs)
- **claw_coder**: 39 programming language references
- **All other agents**: Design, language, math, blockchain references

Civic commands return directly from Chronicle FTS5 in 0.03-0.28s with zero LLM calls.

## LLM Provider Chain (Sovereign Gateway)

| Priority | Provider | Model | Latency | Cost |
|----------|----------|-------|---------|------|
| 1 | Groq | llama-3.3-70b-versatile | 0.7s | Free tier |
| 2 | Ollama | gemma3:4b | 0.8s GPU | Free (local) |
| 3 | OpenRouter | google/gemma-4-26b-a4b-it:free | 0.7s | Free tier |
| 4 | Anthropic | claude-haiku-4-5-20251001 | 1.2s | Paid |

Switch at runtime: llmclaw> /use groq
GPU: GTX 970, 4GB VRAM. Fits: gemma3:4b (3.3GB). Does NOT fit: deepseek-r1:8b (5.2GB).

## File Organization
```
clawpack_v2/
  a2a_server.py          Central message bus (port 8766)
  clawpack.py             Interactive menu
  shared/                 85 shared modules
    llm/client.py         Sovereign Gateway
    base_agent.py         Foundation class (cached_search, ask_llm, call_agent)
    search_cache.py       DataClaw cache engine
    lifecycle.py          Agent cleanup supervisor (0 errors)
  agents/                 21 specialized agents
    webclaw/              BM25 retrieval, Chronicle owner
    dataclaw/             Cache storage + local data retrieval
    lawclaw/              Gold standard reference implementation
    mediclaw/             Hospital geolocation + 91 specialties
    txclaw/               TX.org blockchain (135 URLs + 529 local files)
    ... 16 more agents
  runtime/
    chronicle.db          448MB SQLite FTS5
    ledgers/              Constitutional ledger
  models/
    active_model.json     Active model + provider config
```
