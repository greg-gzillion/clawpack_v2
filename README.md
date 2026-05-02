# 🦞 CLAWPACK V2

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19713157.svg)](https://doi.org/10.5281/zenodo.19713157)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0001--9191--5556-a6ce39?logo=orcid)](https://orcid.org/0009-0001-9191-5556)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)

**21 agents · 6 shared ministries · Sovereign LLM governance · Chronicle audit (35K+) · A2A routing**

---

## 🏛️ Shared Ministries

Every agent inherits these through shared/. No agent works alone.

| Ministry | Path | Purpose |
|----------|------|---------|
| **Sovereign Gateway** | shared/llm/ | All model access. Budget, audit, fallback. 4 providers, 25 models. |
| **Judiciary** | shared/enforcement/ | 19 forbidden patterns. Pre/post execution gates. Recursion guard. |
| **Unified Memory** | shared/memory/ | Chronicle-backed. Cross-agent recall. Auto-extraction from interactions. |
| **Imperial Documents** | shared/files/ | File format conversion. 52 extensions, 8 categories. Batch operations. |
| **DocuClaw API** | shared/docuclaw_api.py | Document creation for all agents. Any agent → DocuClaw for documents. |
| **Agent Registry** | shared/registry.py | 14 agents registered. Capability map. Delegation routing. |
| **Truth Resolver** | shared/truth_resolver.py | Epistemic constitution. web_verified > chronicle > memory > inference. |
| **Source Registry** | shared/source_registry.py | 40+ trusted sources. 4 tiers. Domain-specific overrides. |
| **Execution Policy** | shared/execution_policy.py | Hard boundaries. Delete blocked. Shell blocked. Force push blocked. |
| **Guarded Executor** | shared/guarded_executor.py | Only legal path for dangerous operations. Checks policy + logs to ledger. |
| **Decision Ledger** | shared/decision_ledger.py | Tamper-evident hash chain. Cryptographically verifiable audit trail. |
| **Import Scanner** | shared/import_scanner.py | Detects subprocess, os.system, shell=True bypass attempts. |
| **Memory Guard** | shared/memory_guard.py | Inference never persists. Confidence must exceed 0.75 threshold. |
| **Direct Model Provider** | shared/llm/providers/direct_model.py | Loads obliterated safetensors from disk. No Ollama. No duplication. True sovereignty. |

## 🤖 Agents (21)

| Agent | Domain | Delegates To |
|-------|--------|-------------|
| **llmclaw** | Model management & orchestration | Sovereign gateway |
| **claw_coder** | 39-language code generation | DocuClaw, FileClaw, WebClaw |
| **mathematicaclaw** | Math engine · SymPy · Plotly | DocuClaw (math papers), PlotClaw |
| **mediclaw** | Medical analysis · 66 specialties | DocuClaw (reports), WebClaw |
| **lawclaw** | Law research & analysis | DocuClaw (contracts/briefs), WebClaw |
| **webclaw** | Web search & indexing | Chronicle |
| **dataclaw** | Data search & analysis | FileClaw |
| **docuclaw** | Document creation for ALL agents | FileClaw (format conversion) |
| **fileclaw** | File operations · 52 formats | DocuClaw (documents) |
| **drawclaw** | Visual art & illustration | DocuClaw |
| **plotclaw** | Charts, graphs, data viz | DocuClaw |
| **flowclaw** | Diagrams & flowcharts | DocuClaw |
| **designclaw** | Brand & design | DocuClaw |
| **draftclaw** | Technical drawings | DocuClaw |
| **dreamclaw** | AI vision & generation | Sovereign gateway |
| **interpretclaw** | Translation · 39 languages | WebClaw |
| **langclaw** | Language teaching | WebClaw |
| **crustyclaw** | Rust AI & compiler | ClawCoder |
| **liberateclaw** | Model obliteration | Sovereign gateway |
| **rustypycraw** | Code crawler & analyzer | FileClaw |
| **txclaw** | Blockchain & smart contracts | DocuClaw, FileClaw |

---

## 🧠 LLM Models (25 via sovereign gateway)

**4 providers:** Ollama (local) · Groq · OpenRouter · Anthropic

**Obliterated:** deepseek-coder-liberated · codellama-liberated · smollm2-liberated · tinyllama-liberated · gemma3-liberated

**Active:** qwen3-coder:30b (controlled by llmclaw /use system-wide)

---

## 🏗️ Architecture

clawpack_v2/
├── a2a_server.py # Central A2A server (port 8766)
├── shared/ # UNIVERSAL MINISTRIES
│ ├── llm/ # Sovereign Gateway (12 files)
│ ├── enforcement/ # Judiciary (7 files, 19 patterns)
│ ├── memory/ # Unified Knowledge
│ ├── files/ # Imperial Documents (52 formats)
│ ├── docuclaw_api.py # Document creation for all agents
│ ├── registry.py # Agent capability map & delegation
│ └── base_agent.py # Foundation class for all 21 agents
├── agents/ # 21 specialized agents
├── core/ # System core (adapters only)
├── models/ # LLM storage
├── data/ # Chronicle + budget + memory index
└── exports/ # Generated files

text

## 🔗 A2A Protocol

**Server:** 2a_server.py · **Port:** 8766

`ash
python a2a_server.py
Endpoints: GET /health · GET /v1/agents · GET /memory/stats · POST /v1/message/{agent}

⚖️ Constitutional Law
No agent may speak to a model directly.

All model access routes through shared/llm/client.py. Enforced by pre-commit hook, enforcement engine, and 9 sovereignty patterns. Every call is audited, budgeted, and governed.

MIT License · greg-gzillion
