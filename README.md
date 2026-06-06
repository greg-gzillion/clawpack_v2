# Clawpack V2

A local multi-agent AI runtime. 21 specialized agents communicate through a
central message bus with constitutional governance. Runs on your machine.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19713157.svg)](https://doi.org/10.5281/zenodo.19713157)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)

**21 agents · 90+ shared systems · Chronicle FTS5 (35K+) · A2A routing · BM25 retrieval · Voice/STT/TTS/Braille**

---

## Quickstart (AI Agents: Read This First)

```bash
python scripts/scan.py          # System health check
python scripts/onboard.py        # Full system documentation
python scripts/validate_agents.py # Test all 21 agents
```

Then read: CLAWPACK_ONBOARD.md -> docs/KNOWN_TRAPS.md -> docs/NEXT_SESSION_MISSION.md -> POWERSHELL_SURVIVAL_GUIDE.md

---

## Why Clawpack Exists

Most AI tools are single-model chatbots behind API paywalls. Clawpack is
different: 21 agents with defined jurisdictions, cross-agent delegation,
voice/braille/translation accessibility, BM25 retrieval with source confidence
scoring, and constitutional governance. Runs locally with Ollama. Also works
with Groq, Anthropic, and OpenRouter.

---

## Runtime Health (June 5, 2026)

| Metric | Value |
|--------|-------|
| Agent availability | 21/21 responsive |
| Validation | 21/21 agents pass |
| A2A transport | Healthy (port 8766) |
| Chronicle index | 35,000+ interactions |
| LLM providers | 4/4 operational |
| Provider chain | Groq -> Ollama -> OpenRouter -> Anthropic |
| Active model | llama-3.3-70b-versatile (Groq, 0.7s) |
| BM25 retrieval | Active with source confidence scoring |
| Lifecycle cleanup errors | 0 |
| Voice/listen/translate/braille | 21/21 agents |

---

## Quick Start

```bash
# Install Ollama and pull a model
ollama pull gemma3:4b

# Install dependencies
pip install -r requirements.txt

# Terminal 1: Start the server
python a2a_server.py

# Terminal 2: Launch the menu
python clawpack.py
```

Type 1 for the legal agent. Try `/court Denver CO` or `/help`.

---

## Architecture

### Retrieval Pipeline
```
User Query -> Agent Handler -> _gather_context() -> cached_search()
  -> DataClaw Cache -> (miss) WebClaw BM25 -> Chronicle FTS5
  -> final_score = bm25_score * source_weight
  -> Context -> ask_llm() -> Response
```

### System Tiers

| Tier | Systems | Purpose |
|------|---------|---------|
| Constitutional | lifecycle, enforcement, guarded_executor | Execution safety |
| Retrieval | WebClaw BM25, Chronicle FTS5, DataClaw cache | Knowledge access |
| Intelligence | smart_router, agent_router | Task routing |
| Governance | budget, rate_limiter, error_handler, metrics | Resource protection |
| Memory | memory_guard, source_registry, truth_resolver | Knowledge integrity |
| Infrastructure | input_handler, permissions, registry, event_bus | System services |
| Accessibility | accessibility.py, speech.py, locale.py | Voice, TTS, STT, Braille |

**Truth hierarchy**: web_verified > chronicle > memory > inference.
Lower-tier facts cannot override higher-tier sources.

**LLM access**: Sovereign Gateway only (shared/llm/client.py).
No agent imports LLM libraries directly. Article I — enforced.

---

## The Agents

### Domain Specialists

| # | Agent | Domain |
|---|-------|--------|
| 1 | lawclaw | Legal research, court lookup, case law |
| 4 | mathematicaclaw | Math, calculus, equations |
| 7 | interpretclaw | Translation (42 languages) |
| 8 | langclaw | Language teaching |
| 9 | claw_coder | Code generation (39 languages) |
| 14 | mediclaw | Medical analysis, hospital lookup |
| 15 | dreamclaw | AI vision and generation |
| 16 | designclaw | Graphic design, logos |
| 17 | draftclaw | Technical drawings, blueprints |
| 18 | crustyclaw | Rust programming specialist |
| 20 | drawclaw | AI drawing and art |

### System Utilities

| # | Agent | Domain |
|---|-------|--------|
| 2 | flowclaw | Diagrams, flowcharts, mindmaps |
| 3 | docuclaw | Document creation, PDF export |
| 10 | dataclaw | Data processing, local search, cache storage |
| 11 | webclaw | Web search, Chronicle indexing, BM25 retrieval |
| 12 | fileclaw | File operations, format conversion |
| 13 | plotclaw | Charts and graphs |
| 19 | rustypycraw | Code analysis and crawling |

### System Infrastructure

| # | Agent | Domain |
|---|-------|--------|
| 5 | liberateclaw | Model liberation and management |
| 6 | txclaw | TX.org blockchain |
| 21 | llmclaw | Model selection, Sovereign Gateway |

---

## Honest Limitations

- **LLM speed**: Local inference on CPU is slow. Groq cloud API is fast (0.7s, free tier).
- **Jurisdiction coverage**: 3,800+ cities populated. Some states still incomplete.
- **Cache population**: Infrastructure exists. Only lawclaw actively using cache.
- **Enforcement**: 6 sovereignty patterns actively blocked at HTTP boundary (403).
  Full enforcement pipeline (Pre/PostExecutionGate) still dormant.
- **BM25 visibility**: Retrieval works for all agents. Output format differs between
  agents that return raw results vs those routing through LLM formatting.

---

## Documentation

| File | Purpose |
|------|---------|
| CLAWPACK_ONBOARD.md | Primary reference — architecture, state, debug checklists |
| docs/KNOWN_TRAPS.md | Mistakes that cost hours — read before coding |
| docs/NEXT_SESSION_MISSION.md | Current priorities and migration plan |
| POWERSHELL_SURVIVAL_GUIDE.md | How to work in this environment |
| docs/WEBCLAW_MANUAL.md | WebClaw complete guide |
| docs/WEBCLAW_ARCHITECTURE.md | WebClaw system design |
| shared/CONSTITUTION_v1.md | Supreme law — NON-NEGOTIABLE |
| scripts/validate_agents.py | 21-agent validation harness |
