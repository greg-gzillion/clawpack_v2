# CLAWPACK V2

Policy-enforced local-first multi-agent runtime with audited memory and constitutional execution boundaries. Not an orchestration wrapper around external APIs — a runtime where execution passes through enforced policy gates before agent dispatch.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19713157.svg)](https://doi.org/10.5281/zenodo.19713157)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0001--9191--5556-a6ce39?logo=orcid)](https://orcid.org/0009-0001-9191-5556)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)

**21 agents · 36 shared systems · Chronicle FTS5 (35K+) · A2A routing · Circuit breaker protected**

**Runtime Health:** 20/21 agents loading clean · Chronicle index: 35K+ interactions · A2A port: 8766

---

## What It Does

### Legal Document Drafting — One Command

```bash
lawclaw> /doc service agreement between ABC LLC and XYZ Corp for IT services - governing law Delaware
lawclaw> /translate the contract to German
Structured draft contract generated locally. German translation with legal terms preserved. Three-agent chain executes automatically. Runs on local models.

Clinical Triage + Hospital Routing
bash
mediclaw> /diagnose chest pain in Denver CO
Differential assessment with urgency triage, nearest ER with GPS coordinates, authoritative sources cited.

3,800+ City Civic Database
bash
lawclaw> /jurisdiction Daytona Beach FL
Courts · Police · Jail · Hospitals (GPS) · Library · Building Permits. Shared jurisdiction lookup available across the mesh. Returns from Chronicle FTS5 — no API calls, no latency.

Cross-Agent Mesh
Type /plot bar sales data in lawclaw → routes to plotclaw. Type /code python hello → routes to claw_coder. Any agent accesses any capability. Circuit breaker protected. Task state tracked. Delegation governed by capability registry.

Architecture
36 shared systems in 8 tiers fire on every command through the constitutional handler boundary. LawClaw is the reference implementation at 100% shared infrastructure utilization.

TierSystemsPurpose
Constitutional Closurelifecycle, enforcement, guarded_executor, execution_policyExecution safety
Cognitionchronicle_helper, procedural_memory, three_tierKnowledge retrieval
Intelligencesmart_router, agent_routerTask routing
Operationalvalidation, log_manager, shutdown, hooksOperations
Governancebudget, rate_limiter, error_handler, metrics, securityResource protection
Memory & Truthmemory_guard, source_registry, truth_resolver, decision_ledger, consensus, auditorKnowledge integrity
Infrastructureinput_handler, permissions, registry, jurisdiction_validator, enforcement/gates, config, constitutional_command, court_rules_schema, decomposer, output_handler, router, compactorSystem services
Telemetryobservability, chronicle_ledgerMonitoring
Truth hierarchy enforced at runtime: web_verified > chronicle > memory > inference. Lower-tier facts cannot override higher-tier sources. Inference-tier facts never persist to shared memory.

LLM access governed by Sovereign Gateway. All model calls route through shared/llm/client.py. Direct API access is constitutionally blocked. Provider chain: Groq → Ollama → OpenRouter → Anthropic. Fallback automatic. Budget enforced.

Quick Start
bash
# Terminal 1: Start A2A server
python a2a_server.py

# Terminal 2: Interactive menu
python clawpack.py
Requires Python 3.12+. Local models via Ollama. Cloud fallback via Groq/OpenRouter/Anthropic (optional, configured in .env).

Documentation
FilePurpose
CLAWPACK_ONBOARD.mdComplete system map
ARCHITECTURE.mdSystem design and data flow
AGENT_CAPABILITIES.mdCapability-to-agent registry
AGENT_TEMPLATE.mdBootstrap a new constitutional agent
A2A_PROTOCOL.mdHow agents communicate
BASEAGENT_GUIDE.mdMethods every agent inherits
CHRONICLE_GUIDE.mdShared knowledge database
DECISION_LOG.mdWhy architectural decisions were made
CONSTITUTIONAL_COMPLIANCE_AUDIT.mdPer-agent constitutional compliance
shared/CONSTITUTION_v1.mdSupreme law (frozen)
Data Licensing
Jurisdictional data, court records, building codes: CC BY 4.0 — See LICENSE-DATA

Software code: MIT License — See LICENSE

DOI: 10.5281/zenodo.19713157
