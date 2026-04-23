# 🦞 CLAWPACK V2

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19713157.svg)](https://doi.org/10.5281/zenodo.19713157)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0001--9191--5556-a6ce39?logo=orcid)](https://orcid.org/0009-0001-9191-5556)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)

**20 agents · WebClaw SQLite index · Chronicle ledger · Three-tier memory · Multi-provider LLM**

---

## 🤖 Agents (21)

| Agent | Purpose |
|-------|---------|
| **llmclaw** | Model selection & multi-provider LLM (Groq → Ollama → OpenRouter) |
| **webclaw** | Knowledge base search · 280MB SQLite index · 1.5M terms · 20,212 files |
| **lawclaw** | Law search · 16,827 reference files · Court systems |
| **claw_coder** | Code generation · 38 languages · WebClaw enrichment |
| **mediclaw** | Medical references · 66 specialties · 1,421 files |
| **mathematicaclaw** | Math solver · sympy engine · Calculus, algebra, plotting |
| **interpretclaw** | Translation · 39 languages · Language detection |
| **langclaw** | Language teaching · TTS/STT · Lessons, practice, vocabulary |
| **flowclaw** | Diagrams & flowcharts · Mermaid generation |
| **designclaw** | Graphic design · Brand identity, mood boards, color palettes |
| **docuclaw** | Document processing · 10 import/export formats · Templates |
| **draftclaw** | Technical drawings · Blueprints, CAD, floorplans |
| **drawclaw** | Drawing & sketching |
| **dreamclaw** | AI vision & image generation prompts |
| **dataclaw** | Local reference manager · Chronicle search |
| **liberateclaw** | Model obliteration · 5 obliterated models |
| **plotclaw** | Charts & graphs · Bar, pie, line, scatter |
| **fileclaw** | File analysis & organization |
| **crustyclaw** | Rust AI assistant · Code compilation · Trauma guard |
| **rustypycraw** | Code crawler & analyzer |
| **txclaw** | Blockchain & smart contracts · TX.org |

---

## 🧠 LLM Models (17)

### Obliterated (No Refusals)
deepseek-coder-liberated · codellama-liberated · smollm2-liberated · 	inyllama-liberated · gemma3-liberated

### Standard
Qwen2.5-Coder · deepseek-coder:6.7b · codellama:7b · deepseek-r1:8b · gemma3:4b · gemma3:1b · 	inyllama:1.1b

### Large (CPU)
gemma3:12b · gemma3:27b · qwen3-coder:30b · qwen3-vl:30b

### Cloud
claude-3-haiku (Anthropic)

---

## 📚 Knowledge Base

**WebClaw SQLite Index:** 280MB · 1.5M search terms · 20,212 reference files

| Category | Files |
|----------|-------|
| lawclaw | 16,827 |
| claw_coder | 1,566 |
| mediclaw | 1,421 |
| langclaw | 259 |
| interpretclaw | 38 |
| docuclaw | 21 |
| flowclaw | 20 |
| mathematicaclaw | 17 |
| txclaw | 15 |

---

## 🔗 A2A Protocol

**Server:** 2a_server.py · **Port:** 8766 · **ThreadingHTTPServer**

`ash
python a2a_server.py
Endpoints:
  GET  /health        - Server health + memory stats
  GET  /v1/agents     - List all agents
  GET  /memory/stats  - Detailed memory statistics
  POST /v1/message/{agent} - Send task to agent
Examples
powershell
# Legal research
{
    "task":  "/stats"
} = @{task="/ask What is habeas corpus?"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8766/v1/message/lawclaw" -Method POST -Body {
    "task":  "/stats"
}

# Medical information
{
    "task":  "/stats"
} = @{task="/med diabetes symptoms"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8766/v1/message/mediclaw" -Method POST -Body {
    "task":  "/stats"
}

# Code generation
{
    "task":  "/stats"
} = @{task="/code fibonacci in Rust"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8766/v1/message/claw_coder" -Method POST -Body {
    "task":  "/stats"
}
🏗️ Architecture
text
clawpack_v2/
├── a2a_server.py          # Central A2A server
├── shared/
│   ├── base_agent.py       # Foundation class for all agents
│   ├── llm/                # Multi-provider LLM (Groq, Anthropic, Ollama, OpenRouter)
│   ├── memory/             # Three-tier (Working, Semantic, Procedural)
│   ├── chronicle_helper.py # WebClaw chronicle integration
│   ├── hooks/              # Agent, command, HTTP, prompt runners
│   └── skills/             # Agent skill definitions
├── agents/                 # 21 specialized agents
├── core/                   # System core (LLM manager, agent loader, fork)
├── models/                 # LLM storage (obliterated + stock)
└── docs/                   # Documentation
Features
Four-Tier Smart Routing — saves tokens on simple commands

Task Decomposer — breaks complex tasks into sub-tasks

Three-Tier Memory — working, semantic, procedural for all agents

Adaptive Budget Controller — smart token management

MCP Registry — install/manage MCP servers

Chronicle Ledger — persistent URL tracking with context

Cross-Learning — agents share knowledge via shared memory

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
