# CLAWPACK V2

Constitutional multi-agent runtime with sovereign model governance, audited memory, and enforced execution law.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19713157.svg)](https://doi.org/10.5281/zenodo.19713157)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0001--9191--5556-a6ce39?logo=orcid)](https://orcid.org/0009-0001-9191-5556)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)

**21 agents · 36 shared systems · Chronicle FTS5 (35K+) · A2A routing · Circuit breaker protected**

---

## What It Does

**Legal Documents — One Command:**
```bash
lawclaw> /doc service agreement between ABC LLC and XYZ Corp for IT services - governing law Delaware
lawclaw> /translate the contract to German
Professional contract in English. German translation with legal terms preserved. Three agents chain automatically. Free on local models.

Medical Intelligence — Diagnosis + Hospital Routing:

bash
mediclaw> /diagnose chest pain in Denver CO
Differential diagnosis with urgency triage, nearest ER with GPS coordinates, authoritative sources cited.

3,800+ City Civic Database:

bash
lawclaw> /jurisdiction Daytona Beach FL
Courts · Police · Jail · Hospitals (GPS) · Library · Building Permits. All 21 agents access via lookup_jurisdiction().

Cross-Agent Mesh:
Type /plot bar sales data in lawclaw → routes to plotclaw. Type /code python hello → routes to claw_coder. Any agent accesses any capability. Circuit breaker protected. Task state tracked.

Architecture
36 shared systems in 8 tiers fire automatically on every command through the constitutional handler boundary.

TierSystemsPurpose
Constitutional Closurelifecycle, enforcement, guarded_executor, execution_policyExecution safety
Cognitionchronicle_helper, procedural_memory, three_tierKnowledge retrieval
Intelligencesmart_router, agent_routerTask routing
Operationalvalidation, log_manager, shutdown, hooksOperations
Governancebudget, rate_limiter, error_handler, metrics, securityResource protection
Memory & Truthmemory_guard, source_registry, truth_resolver, decision_ledger, consensus, auditorKnowledge integrity
Infrastructureinput_handler, permissions, registry, jurisdiction_validator, enforcement/gates, config, constitutional_command, court_rules_schema, decomposer, output_handler, router, compactorSystem services
Telemetryobservability, chronicle_ledgerMonitoring
Quick Start
bash
python a2a_server.py    # Terminal 1: Start A2A server (port 8766)
python clawpack.py       # Terminal 2: Interactive menu
Documentation
CLAWPACK_ONBOARD.md — Complete system map

ARCHITECTURE.md — System design and data flow

AGENT_CAPABILITIES.md — Capability-to-agent registry

AGENT_TEMPLATE.md — Bootstrap a new constitutional agent

A2A_PROTOCOL.md — How agents communicate

BASEAGENT_GUIDE.md — Methods every agent inherits

CHRONICLE_GUIDE.md — Shared knowledge database

DECISION_LOG.md — Why architectural decisions were made

shared/CONSTITUTION_v1.md — Supreme law (frozen)

Data Licensing
Jurisdictional data, court records, building codes: CC BY 4.0. See LICENSE-DATA.
Software code: MIT License. See LICENSE.
DOI: 10.5281/zenodo.19713157
