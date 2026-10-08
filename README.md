# Clawpack V2

A local multi-agent AI runtime. 21 specialized agents communicate through a
central message bus with constitutional governance. Runs on your machine.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19713157.svg)](https://doi.org/10.5281/zenodo.19713157)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)

**21 agents · 90+ shared systems · Chronicle FTS5 (237K+) · A2A routing · BM25 retrieval · Voice/STT/TTS/Braille**

---

## Quickstart (AI Agents: Read This First)

```bash
python scripts/scan.py             # System health check
python scripts/onboard.py          # Full system documentation
python scripts/validate_agents.py  # Test all 21 agents
Then read, in order:

CLAWPACK_ONBOARD.md — architecture, state, debug checklists

docs/KNOWN_TRAPS.md — mistakes that cost hours

docs/NEXT_SESSION_MISSION.md — current priorities

POWERSHELL_SURVIVAL_GUIDE.md — how to work in this environment

Why Clawpack Exists
Most AI tools are single-model chatbots behind API paywalls. Clawpack is
different: 21 agents with defined jurisdictions, cross-agent delegation,
voice/braille/translation accessibility, BM25 retrieval with source confidence
scoring, and constitutional governance.

Runs locally with Ollama. Also works with Groq, Anthropic, OpenRouter, and
OpenAI. Current default is Groq (openai/gpt-oss-20b) for speed.

Runtime Health (October 8, 2026)
Metric	Value
Agent availability	21/21 responsive
Validation	21/21 agents pass
A2A transport	Healthy (port 8766)
Chronicle index	237,878 interactions
LLM providers	5 detected (Groq, Ollama, OpenRouter, Anthropic, OpenAI)
Provider chain	Groq -> Ollama -> direct_model -> OpenRouter -> Anthropic
Active model	openai/gpt-oss-20b (Groq, ~0.35s)
BM25 retrieval	Active with source confidence scoring
Lifecycle cleanup errors	0
Voice/listen/translate/braille	21/21 agents
Note: direct_model (phi2) is currently broken (missing AutoModelForCausalLM
import). It should be removed or repaired in a future session. Effective
fallback chain when Groq is unavailable: Ollama (if running) -> OpenRouter
(rate-limited) -> Anthropic.

Quick Start
One-command launcher (recommended)
bash
# Install dependencies (core)
pip install -r requirements.txt

# Optional: audio (langclaw TTS/STT, lawclaw voice)
pip install -r requirements-audio.txt

# Optional: accessibility (lawclaw braille, global hotkeys)
pip install -r requirements-accessibility.txt

# Launch everything — server + menu
python run.py
run.py starts the A2A server, waits for it to become healthy, then launches
the menu. Exit the menu to shut down the server.

Two-terminal (development)
bash
# Terminal 1: Start the server
python a2a_server.py

# Terminal 2: Launch the menu
python clawpack.py
Type 1 for the legal agent. Try /court Denver CO or /help.

Optional: Local LLM (Ollama)
If you want fully local inference:

bash
ollama pull gemma3:4b
Set ollama.priority to 1 in models/active_model.json to prefer local
inference over Groq.

Architecture
Retrieval Pipeline
text
User Query -> Agent Handler -> _gather_context() -> cached_search()
  -> DataClaw Cache -> (miss) WebClaw BM25 -> Chronicle FTS5
  -> final_score = bm25_score * source_weight
  -> Context -> ask_llm() -> Response
System Tiers
Tier	Systems	Purpose
Constitutional	lifecycle, enforcement, guarded_executor	Execution safety
Retrieval	WebClaw BM25, Chronicle FTS5, DataClaw cache	Knowledge access
Intelligence	smart_router, agent_router	Task routing
Governance	budget, rate_limiter, error_handler, metrics	Resource protection
Memory	memory_guard, source_registry, truth_resolver	Knowledge integrity
Infrastructure	input_handler, permissions, registry, event_bus	System services
Accessibility	accessibility.py, speech.py, locale.py	Voice, TTS, STT, Braille
Truth hierarchy: web_verified > chronicle > memory > inference.
Lower-tier facts cannot override higher-tier sources.

LLM access: Sovereign Gateway only (shared/llm/client.py).
No agent imports LLM libraries directly. Article I — enforced.

The Agents
Domain Specialists
#	Agent	Domain
1	lawclaw	Legal research, court lookup, case law
4	mathematicaclaw	Math, calculus, equations
7	interpretclaw	Translation (42 languages)
8	langclaw	Language teaching
9	claw_coder	Code generation (39 languages)
14	mediclaw	Medical analysis, hospital lookup
15	dreamclaw	AI vision and generation
16	designclaw	Graphic design, logos
17	draftclaw	Technical drawings, blueprints
18	crustyclaw	Rust programming specialist
20	drawclaw	AI drawing and art
System Utilities
#	Agent	Domain
2	flowclaw	Diagrams, flowcharts, mindmaps
3	docuclaw	Document creation, PDF export
10	dataclaw	Data processing, local search, cache storage
11	webclaw	Web search, Chronicle indexing, BM25 retrieval
12	fileclaw	File operations, format conversion
13	plotclaw	Charts and graphs
19	rustypycraw	Code analysis and crawling
System Infrastructure
#	Agent	Domain
5	liberateclaw	Model liberation and management
6	txclaw	TX.org blockchain
21	llmclaw	Model selection, Sovereign Gateway
Project Structure
text
clawpack_v2/
├── a2a_server.py            A2A HTTP server (stdlib http.server, port 8766)
├── run.py                   One-command launcher (server + menu)
├── clawpack.py              Interactive menu
├── claw.py                  Direct single-agent launcher (dev)
├── agents/                  21 agents, one directory each
│   ├── lawclaw/
│   ├── webclaw/             Shared retrieval layer
│   ├── dataclaw/            Local FTS5 file index
│   └── ...
├── shared/                  Cross-agent systems
│   ├── llm/                 Sovereign Gateway (only path to LLMs)
│   ├── memory/              mem0-backed unified memory
│   ├── query_normalizer.py  Geographic extraction
│   └── ...
├── runtime/                 Persistence
│   ├── chronicle.db         FTS5 index (237K rows, ~590 MB)
│   ├── mem0/                Qdrant vector store
│   └── ledgers/             Constitutional + chronicle ledgers
├── scripts/                 Utility scripts (onboard, scan, validate, rebuild_data_index)
├── models/
│   └── active_model.json    Provider priorities and active model
└── requirements*.txt        Split by feature group
Honest Limitations
LLM speed: Local inference on CPU is slow. Groq cloud API is fast
(~0.35s, free tier but rate-limited).

Groq rate limits: Free tier throttles bursts. Sequential validation
may occasionally hit 429s.

Jurisdiction coverage: 3,800+ cities populated. Some states incomplete.

Cache population: Infrastructure exists. Only lawclaw actively uses cache.

Enforcement: 6 sovereignty patterns actively blocked at HTTP boundary (403).
Full enforcement pipeline (Pre/PostExecutionGate) still dormant.

BM25 visibility: Retrieval works for all agents. Output format differs
between agents that return raw results vs those routing through LLM formatting.

Deferred work: _gather_context() migration (Pattern A → Pattern B),
datetime.utcnow() deprecation fix, Chronicle deduplication.

Documentation
File	Purpose
CLAWPACK_ONBOARD.md	Primary reference — architecture, state, debug checklists
docs/KNOWN_TRAPS.md	Mistakes that cost hours — read before coding
docs/NEXT_SESSION_MISSION.md	Current priorities and migration plan
POWERSHELL_SURVIVAL_GUIDE.md	How to work in this environment
docs/WEBCLAW_MANUAL.md	WebClaw complete guide
docs/WEBCLAW_ARCHITECTURE.md	WebClaw system design
shared/CONSTITUTION_v1.md	Supreme law — NON-NEGOTIABLE
SECURITY.md	Vulnerability reporting
CONTRIBUTING.md	How to contribute
scripts/validate_agents.py	21-agent validation harness
Contributing
Bug reports, fixes, and pull requests are welcome. See
CONTRIBUTING.md for guidelines.

For security issues, do not open a public issue. See
SECURITY.md for the responsible disclosure process.

Citation
If you use Clawpack in academic work, cite via Zenodo:

bibtex
@software{clawpack_v2,
  doi = {10.5281/zenodo.19713157},
  url = {https://doi.org/10.5281/zenodo.19713157}
}
See CITATION.cff for full details.

License
MIT — see LICENSE.

Last updated: 2026-10-08

text

---

## What Changed vs. Your Original

| Section | Change |
|---------|--------|
| Header badge line | `35K+` → `237K+` |
| Quickstart commands | Kept (still accurate) |
| "Why Clawpack Exists" | "Runs locally with Ollama. Also works with Groq..." → "Runs locally with Ollama. Also works with Groq, Anthropic, OpenRouter, and OpenAI. Current default is Groq..." |
| Runtime Health date | `June 5, 2026` → `October 8, 2026` |
| Runtime Health — Chronicle | `35,000+` → `237,878` |
| Runtime Health — providers | `4/4` → `5 detected` |
| Runtime Health — chain | Corrected to include `direct_model` |
| Runtime Health — model | `llama-3.3-70b-versatile` → `openai/gpt-oss-20b` |
| Runtime Health — note | Added note about broken `direct_model` |
| Quick Start | Added `run.py` as recommended path; kept two-terminal as dev path; added `ollama pull` as optional |
| Architecture — Retrieval Pipeline | Unchanged (accurate) |
| Architecture — System Tiers | Unchanged (accurate) |
| Agents tables | Unchanged (accurate) |
| Project Structure | **New section** — helps readers find files |
| Honest Limitations | Updated with Groq rate limits + deferred work |
| Documentation | Added SECURITY.md and CONTRIBUTING.md |
| Contributing | **New section** |
| Citation | **New section** |
| License | **New section** |
| Footer | Added `Last updated: 2026-10-08` |

---

## Before You Save

**Two things to verify:**

**1. Does `CONTRIBUTING.md` exist?**

I referenced it in the new README. Your `ls` earlier showed `CONTRIBUTING.md` at the root — but let me be sure it's populated, not a stub:

```powershell
cd C:\Users\greg\dev\clawpack_v2
Get-Content CONTRIBUTING.md| 5 | liberateclaw | Model liberation and management |
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
