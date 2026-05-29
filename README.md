# CLAWPACK V2

Constitutional multi-agent runtime with sovereign model governance, audited memory, and enforced execution law.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19713157.svg)](https://doi.org/10.5281/zenodo.19713157)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0001--9191--5556-a6ce39?logo=orcid)](https://orcid.org/0009-0001-9191-5556)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)

**21 agents · 15 sovereign ministries · Chronicle audit (35K+) · A2A routing**

---

## What It Does

**Bilingual Legal Documents — One Command:**
ash
lawclaw> /doc service agreement between ABC LLC and XYZ Corp for IT services - effective date June 1 2026 - payment /hr net 30 - governing law Delaware
lawclaw> /translate the contract to German

→ Professional contract in English. Then a complete German translation with all legal terms preserved (Latin, French, citations, party names, court names). Three agents chain automatically. Free on local models.

**Jurisdiction-Compliant Court Filings:**
ash
lawclaw> /doc motion to dismiss Miami FL - plaintiff: John Smith - defendant: ABC Corp - case: 2024-CV-1234 - grounds: failure to state a claim

→ Filing-ready motion with correct court (11th Judicial Circuit), Florida Rule 1.140(b)(6), proper caption, and authoritative .gov sources at 0.92 trust.

**Cross-Agent Mesh:**
Type /plot bar sales data in lawclaw → silently routes to plotclaw. Type /code python hello world → routes to claw_coder. Any agent accesses any capability without knowing the commands exist.

**Self-Improving Knowledge:**
ash
lawclaw> /law qualified immunity
  [MEMORY] 3 related prior searches found
  31,918 cases found · 8 displayed
  SCOTUS: Pearson v. Callahan (2009)

lawclaw> /correct salazar-limon url https://www.oyez.org/cases/2016/15-617
  Correction recorded. Truth score: 0.29 (builds with confirmations)

→ The system learns from every interaction. Corrections build consensus over time. Facts carry staleness warnings.

**3,800+ City Civic Database:**
ash
lawclaw> /jurisdiction Daytona Beach FL
  Courts · Police · Jail · 2 Hospitals (GPS) · Library · Building Permits

→ Complete municipal data for every US city. All CC BY 4.0 licensed. DOI: 10.5281/zenodo.19713157.

---

## Architecture

> No agent may speak to a model directly.

### Sovereign Ministries

Every agent inherits these through shared/. No agent works alone.

| Ministry | Path | Purpose |
|----------|------|---------|
| **Sovereign Gateway** | shared/llm/ | All model access. Budget, audit, fallback. 4 providers, 25 models. |
| **Judiciary** | shared/enforcement/ | 19 forbidden patterns. Pre/post execution gates. |
| **Unified Memory** | shared/memory/ | Chronicle-backed. Cross-agent recall. |
| **Truth Resolver** | shared/truth_resolver.py | web_verified > chronicle > memory > inference |
| **Source Registry** | shared/source_registry.py | 40+ trusted sources. 4 tiers. .gov at 0.92 authoritative |
| **Consensus Engine** | shared/consensus_engine.py | Reputation-based fact scoring across agents |
| **Decision Ledger** | shared/decision_ledger.py | Tamper-evident hash chain. Verifiable audit. |
| **Guarded Executor** | shared/guarded_executor.py | Only legal path for dangerous operations. |
| **Memory Guard** | shared/memory_guard.py | Inference never persists. Confidence >= 0.75. Staleness warnings. |
| **Agent Helpers** | shared/_agent_helpers.py | Shared execution substrate connecting all 21 agents. |

### Agents (21)

| Agent | Domain | Delegates To |
|-------|--------|-------------|
| **lawclaw** | Law research, documents, translation (25 commands) | DocuClaw, WebClaw, PlotClaw, FlowClaw, InterpretClaw |
| **llmclaw** | Model management and orchestration | Sovereign gateway |
| **claw_coder** | 39-language code generation | DocuClaw, FileClaw, WebClaw |
| **mathematicaclaw** | Math engine · SymPy · Plotly | DocuClaw, PlotClaw |
| **mediclaw** | Medical analysis · 66 specialties | DocuClaw, WebClaw, LawClaw |
| **webclaw** | Web search and indexing | Chronicle |
| **dataclaw** | Data search and analysis | FileClaw |
| **docuclaw** | Document creation for ALL agents | FileClaw, InterpretClaw |
| **fileclaw** | File operations · 52 formats | DocuClaw |
| **drawclaw** | Visual art and illustration | DocuClaw |
| **plotclaw** | Charts, graphs, data viz | DocuClaw |
| **flowclaw** | Diagrams and flowcharts | DocuClaw, WebClaw, DataClaw, FileClaw |
| **designclaw** | Brand and design | DocuClaw |
| **draftclaw** | Technical drawings | DocuClaw |
| **dreamclaw** | AI vision and generation | Sovereign gateway |
| **interpretclaw** | Translation · 39 languages | WebClaw |
| **langclaw** | Language teaching | WebClaw |
| **crustyclaw** | Rust AI and compiler | ClawCoder |
| **liberateclaw** | Model obliteration | Sovereign gateway |
| **rustypycraw** | Code crawler and analyzer | WebClaw, DataClaw, CrustyClaw, ClawCoder |
| **txclaw** | Blockchain and smart contracts | DocuClaw, FileClaw |

### Quick Start
ash
python a2a_server.py    # Terminal 1: Start A2A server
python clawpack.py       # Terminal 2: Interactive menu

**Endpoints:** GET /health · GET /v1/agents · GET /memory/stats · POST /v1/message/{agent}

### Documentation
- CLAWPACK_ONBOARD.md — Complete system map for AI agents and developers
- CONSTITUTIONAL_COMPLIANCE_AUDIT.md — Reproducible constitutional audit
- AGENT_TEMPLATE.md — Bootstrap a new constitutional agent in minutes
- AGENT_CAPABILITIES.md — Complete capability-to-agent registry
- DECISION_LOG.md — Why architectural decisions were made
- ARCHITECTURE.md — System design and data flow
- shared/CONSTITUTION_v1.md — Supreme law (frozen)

## Constitutional Law
All model access routes through shared/llm/client.py. Enforced by pre-commit hook, enforcement engine, and 9 sovereignty patterns. Every call is audited, budgeted, and governed. Every command passes through 23-system constitutional boundary automatically.

## Data Licensing Notice (Effective May 4, 2026)
All jurisdictional data, court records, building codes, and design resources in this repository are licensed under CC BY 4.0. See LICENSE-DATA for full terms.

Suggested attribution: Data sourced from Clawpack V2 Jurisdictional Dataset (github.com/greg-gzillion/clawpack_v2), used under CC BY 4.0.

DOI: 10.5281/zenodo.19713157 (latest version via Zenodo)

MIT License · greg-gzillion
