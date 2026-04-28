# 🦞 CLAWPACK V2

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19713157.svg)](https://doi.org/10.5281/zenodo.19713157)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0001--9191--5556-a6ce39?logo=orcid)](https://orcid.org/0009-0001-9191-5556)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)

**21 agents · SQLite Chronicle (136K cards) · FTS5 Search · Multi-provider LLM · A2A Routing**

---

## 🤖 Agents (21)

| Agent | Purpose |
|-------|---------|
| **llmclaw** | Model management & orchestration · 17 models · cloud + local |
| **claw_coder** | 39-language code generator · compiler validation · code translation · project scaffolding |
| **mathematicaclaw** | Math engine · SymPy · Plotly animations · step-by-step calculus · 17 commands |
| **mediclaw** | Medical references · 66 specialties · chronicle-backed citations · 22 commands |
| **lawclaw** | Law research · court systems · case law · chronicle search |
| **webclaw** | Web search & indexing · SQLite index · chronicle ledger · URL fetching |
| **dataclaw** | Local data search · file scanning · JSON/CSV search · chronicle integration |
| **docuclaw** | Document generator · 21 format exports · templates · translation · combine/convert |
| **fileclaw** | File handler · 52 formats (import/export/convert) · EPUB support |
| **designclaw** | Brand & design · brand kits · color palettes · HTML generation |
| **flowclaw** | Diagrams & flowcharts · Mermaid generation · browser viewer |
| **crustyclaw** | Rust AI · compiler validation · cargo integration · standalone binary bridge |
| **interpretclaw** | Translation · 39 languages · language detection |
| **langclaw** | Language teaching · TTS/STT · lessons, practice, vocabulary |
| **draftclaw** | Technical drawings · blueprints, CAD, floorplans |
| **drawclaw** | Drawing & sketching |
| **dreamclaw** | AI vision & image generation |
| **plotclaw** | Charts & graphs · bar, pie, line, scatter |
| **liberateclaw** | Model obliteration · 5 obliterated models |
| **rustypycraw** | Code crawler & analyzer |
| **txclaw** | Blockchain & smart contracts |

---

## 🧠 LLM Models (17)

**Obliterated (No Refusals):** deepseek-coder-liberated · codellama-liberated · smollm2-liberated · tinyllama-liberated · gemma3-liberated

**Standard:** Qwen2.5-Coder · deepseek-coder:6.7b · codellama:7b · deepseek-r1:8b · gemma3:4b · gemma3:1b · tinyllama:1.1b

**Large (Local):** gemma3:12b · gemma3:27b · qwen3-coder:30b · qwen3-vl:30b

**Cloud:** claude-haiku-4-5-20251001 (Anthropic) · llama-3.1-8b-instant (Groq)

---

## 📚 Chronicle Index

**SQLite database** · 136,435 cards · FTS5 full-text search · 22,883 files indexed with full content

Every `.md` file in `agents/webclaw/references/` is indexed with title, content, and URLs. All agents search it via `BaseAgent.search_chronicle()`.

---

## 🔗 A2A Protocol

**Server:** `a2a_server.py` · **Port:** 8766

```bash
python a2a_server.py
Endpoints:

GET /health — Server health + memory stats

GET /v1/agents — List all agents

GET /memory/stats — Detailed memory statistics

POST /v1/message/{agent} — Send task to agent

🏗️ Architecture
text
clawpack_v2/
├── a2a_server.py          # Central A2A server
├── shared/
│   ├── base_agent.py       # Foundation class for all agents
│   ├── llm/                # Multi-provider LLM
│   ├── memory/             # Three-tier memory
│   └── hooks/              # Agent, command, HTTP, prompt runners
├── agents/                 # 21 specialized agents
├── core/                   # System core
├── models/                 # LLM storage
├── data/                   # Chronicle database + shared memory
└── exports/                # Generated files
📚 Citation
APA
Frank, G. (2026). Clawpack V2 (Version 3.0.0) [Computer software]. https://doi.org/10.5281/zenodo.19713157

BibTeX

bibtex
@software{frank_clawpack_v2_2026,
  author       = {Greg Frank},
  title        = {Clawpack V2},
  version      = {3.0.0},
  year         = {2026},
  doi          = {10.5281/zenodo.19713157},
  url          = {https://github.com/greg-gzillion/clawpack_v2}
}
MIT License · greg-gzillion