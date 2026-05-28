# CLAWPACK V2

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19713157.svg)](https://doi.org/10.5281/zenodo.19713157)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0001--9191--5556-a6ce39?logo=orcid)](https://orcid.org/0009-0001-9191-5556)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)

**21 agents · 6 shared ministries · Sovereign LLM governance · Chronicle audit (35K+) · A2A routing**

---

## Shared Ministries

Every agent inherits these through shared/. No agent works alone.

| Ministry | Path | Purpose |
|----------|------|---------|
| **Sovereign Gateway** | shared/llm/ | All model access. Budget, audit, fallback. 4 providers, 25 models. |
| **Judiciary** | shared/enforcement/ | 19 forbidden patterns. Pre/post execution gates. Recursion guard. |
| **Unified Memory** | shared/memory/ | Chronicle-backed. Cross-agent recall. All 23 lawclaw commands wired. |
| **Imperial Documents** | shared/files/ | File format conversion. 52 extensions, 8 categories. Batch operations. |
| **DocuClaw API** | shared/docuclaw_api.py | Document creation for all agents. Any agent to DocuClaw. |
| **Agent Registry** | shared/registry.py | 21 agents registered. Capability map. Delegation routing. |
| **Truth Resolver** | shared/truth_resolver.py | Epistemic constitution. web_verified > chronicle > memory > inference. |
| **Source Registry** | shared/source_registry.py | 40+ trusted sources. 4 tiers. Domain-specific overrides. |
| **Execution Policy** | shared/execution_policy.py | Hard boundaries. Delete blocked. Shell blocked. Force push blocked. |
| **Guarded Executor** | shared/guarded_executor.py | Only legal path for dangerous operations. Checks policy + logs to ledger. |
| **Decision Ledger** | shared/decision_ledger.py | Tamper-evident hash chain. Cryptographically verifiable audit trail. |
| **Import Scanner** | shared/import_scanner.py | Detects subprocess, os.system, shell=True bypass attempts. |
| **Memory Guard** | shared/memory_guard.py | Inference never persists. Confidence must exceed 0.75 threshold. |
| **Direct Model Provider** | shared/llm/providers/direct_model.py | Loads obliterated safetensors from disk. No Ollama. No duplication. True sovereignty. |
| **Agent Helpers** | shared/_agent_helpers.py | Empire-wide utilities. All 21 agents connected. LLM, Chronicle, delegation, memory. |

## Agents (21)

| Agent | Domain | Delegates To |
|-------|--------|-------------|
| **llmclaw** | Model management and orchestration | Sovereign gateway |
| **claw_coder** | 39-language code generation | DocuClaw, FileClaw, WebClaw |
| **mathematicaclaw** | Math engine - SymPy - Plotly | DocuClaw, PlotClaw |
| **mediclaw** | Medical analysis - 66 specialties | DocuClaw, WebClaw, LawClaw |
| **lawclaw** | Law research and analysis (23 commands) | DocuClaw, WebClaw, PlotClaw, FlowClaw |
| **webclaw** | Web search and indexing | Chronicle |
| **dataclaw** | Data search and analysis | FileClaw |
| **docuclaw** | Document creation for ALL agents | FileClaw, InterpretClaw |
| **fileclaw** | File operations - 52 formats | DocuClaw |
| **drawclaw** | Visual art and illustration | DocuClaw |
| **plotclaw** | Charts, graphs, data viz | DocuClaw |
| **flowclaw** | Diagrams and flowcharts | DocuClaw, WebClaw, DataClaw, FileClaw |
| **designclaw** | Brand and design | DocuClaw |
| **draftclaw** | Technical drawings | DocuClaw |
| **dreamclaw** | AI vision and generation | Sovereign gateway |
| **interpretclaw** | Translation - 39 languages | WebClaw |
| **langclaw** | Language teaching | WebClaw |
| **crustyclaw** | Rust AI and compiler | ClawCoder |
| **liberateclaw** | Model obliteration | Sovereign gateway |
| **rustypycraw** | Code crawler and analyzer | WebClaw, DataClaw, CrustyClaw, ClawCoder |
| **txclaw** | Blockchain and smart contracts | DocuClaw, FileClaw |

## LLM Models (25 via sovereign gateway)

**4 providers:** Ollama (local) - Groq - OpenRouter - Anthropic

**Obliterated:** deepseek-coder-liberated - codellama-liberated - smollm2-liberated - tinyllama-liberated - gemma3-liberated

**Active:** claude-haiku-4-5-20251001 (controlled by llmclaw /use system-wide)

## Architecture
clawpack_v2/
├── a2a_server.py # Central A2A server (port 8766)
├── shared/ # UNIVERSAL MINISTRIES
│ ├── llm/ # Sovereign Gateway
│ ├── enforcement/ # Judiciary (7 files, 19 patterns)
│ ├── memory/ # Unified Knowledge
│ ├── files/ # Imperial Documents (52 formats)
│ ├── _agent_helpers.py # Empire-wide bridge (all 21 agents)
│ └── base_agent.py # Foundation class
├── agents/ # 21 specialized agents
├── data/ # Chronicle + budget + memory index
└── exports/ # Generated files

text

## A2A Protocol

**Server:** a2a_server.py - **Port:** 8766

```bash
python a2a_server.py
Endpoints: GET /health - GET /v1/agents - GET /memory/stats - POST /v1/message/{agent}

Constitutional Law
No agent may speak to a model directly. All model access routes through shared/llm/client.py. Enforced by pre-commit hook, enforcement engine, and 9 sovereignty patterns. Every call is audited, budgeted, and governed.

Data Licensing Notice (Effective May 4, 2026)
All jurisdictional data, court records, building codes, and design resources in this repository are licensed under CC BY 4.0. See LICENSE-DATA for full terms.

Clones prior to v3.1.0-data-license were under MIT only. Current and future use requires attribution.

Suggested attribution: Data sourced from Clawpack V2 Jurisdictional Dataset (github.com/greg-gzillion/clawpack_v2), used under CC BY 4.0.

DOI: 10.5281/zenodo.19713157 (latest version via Zenodo)

MIT License - greg-gzillion
