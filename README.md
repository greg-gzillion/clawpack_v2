# CLAWPACK V2

Policy-enforced local-first multi-agent runtime with audited memory and constitutional execution boundaries.

Not an orchestration wrapper around external APIs — a runtime where execution passes through enforced policy gates before agent dispatch.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19713157.svg)](https://doi.org/10.5281/zenodo.19713157)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0001--9191--5556-a6ce39?logo=orcid)](https://orcid.org/0009-0001-9191-5556)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)

**21 agents · 36 shared systems · Chronicle FTS5 (35K+) · A2A routing · Circuit breaker protected**

---

## Runtime Health

| Metric | Value |
|--------|-------|
| Agent availability | 21/21 responsive |
| Median control-path latency | 0.2s |
| A2A transport | Healthy (port 8766) |
| Chronicle index | 35,553 interactions |
| LLM providers | 4/4 operational |
| Provider chain | Groq → Ollama → OpenRouter → Anthropic |
| Lifecycle cleanup errors | 0 (contract drift resolved 2026-05-30) |
| Chronicle search warnings | Non-blocking signature reconciliation in progress |

---

## Execution Flow
User Command
↓
Constitutional Boundary (23-system handler)
↓
Validation + Enforcement Gates
↓
Truth Resolution (web_verified > chronicle > memory > inference)
↓
Capability Router (shared/capabilities.py)
↓
Agent Dispatch (A2A, port 8766)
↓
Chronicle Audit + Memory Commit

text

---

## What It Does

### Legal Document Drafting

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
Courts · Police · Jail · Hospitals (GPS) · Library · Building Permits. Returns from Chronicle FTS5 in under 0.05s — no API calls.

Cross-Agent Mesh
bash
lawclaw> /plot bar sales data     # routes to plotclaw
lawclaw> /code python hello       # routes to claw_coder
Any agent accesses any capability. Circuit breaker protected. Delegation governed by capability registry.

Architecture
36 shared systems organized in tiers. LawClaw is the reference implementation exercising the full constitutional execution stack.

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

LLM access governed by Sovereign Gateway. All model calls route through shared/llm/client.py. Direct API access is blocked by enforcement gates. Provider chain: Groq → Ollama → OpenRouter → Anthropic. Budget enforced.

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
shared/CONSTITUTION_v1.mdConstitutional law (frozen)
Known Active Work
AreaStatus
Chronicle recover_by_context signature normalization19 call sites across 8 modules; non-blocking warnings, no functional impact
Shared memory adoption20 agents need UnifiedMemory bridge (lawclaw is reference implementation)
Enforcement engine activationshared/enforcement/engine.py exists but not wired into A2A request path
Guarded executor wiringshared/guarded_executor.py exists but not called by a2a_server.py
Registry completeness5 agent entries exist in code but outside AGENT_REGISTRY dict closing brace
Benchmark Snapshot (2026-05-30)
MetricValue
Agent /help latency (median)0.2s
Agent /help latency (max)0.5s
Civic command latency (Chronicle FTS5)0.03-0.28s
LLM inference latency (Groq)0.7s
LLM inference latency (Ollama local)0.8s
Chronicle FTS5 entries35,553
Circuit breaker trips0 (no cascading failures)
Lifecycle cleanup errors0
Data Licensing
Jurisdictional data, court records, building codes: CC BY 4.0 — See LICENSE-DATA

Software code: MIT License — See LICENSE

DOI: 10.5281/zenodo.19713157
