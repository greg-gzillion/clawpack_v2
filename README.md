# CLAWPACK V2

Policy-enforced local-first multi-agent runtime with audited memory and constitutional execution boundaries.

Not an orchestration wrapper around external APIs. A runtime where execution passes through enforced policy gates before agent dispatch. Speak any language. Get responses in your language.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19713157.svg)](https://doi.org/10.5281/zenodo.19713157)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0001--9191--5556-a6ce39?logo=orcid)](https://orcid.org/0009-0001-9191-5556)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)

**21 agents · 36 shared systems · Chronicle FTS5 (35K+) · A2A routing · Voice/STT/TTS/Braille · Circuit breaker protected**

---

## Runtime Health

| Metric | Value |
|--------|-------|
| Agent availability | 21/21 responsive |
| Median control-path latency | 0.2s |
| A2A transport | Healthy (port 8766) |
| Chronicle index | 35,553 interactions |
| LLM providers | 4/4 operational |
| Provider chain | Groq -> Ollama -> OpenRouter -> Anthropic |
| Lifecycle cleanup errors | 0 |
| Voice/listen/translate/braille | 21/21 agents |

---

## Getting Started

### Step 1: Start the server
`ash
python a2a_server.py
Step 2: Launch the menu
bash
python clawpack.py
Step 3: Navigate
You see a menu of 21 agents. Choose how to interact:

With keyboard: Type a number (1-21) and press Enter.
With voice: Press v then Enter, or say "start listening". Then say "switch to lawclaw" or "agent four".
With hotkeys: Ctrl+Shift+V toggles voice mode anywhere.

Step 4: Use an agent
Once inside an agent, type /help to see its commands. Every agent supports:

CommandWhat it does
/voiceToggle voice mode (speak instead of type)
/listenOne-shot microphone transcription
/translate <text>Detect language and translate to English
/braille <text>Convert text to Braille output
Step 5: Switch agents
Type exit to return to the menu. Pick another agent.

Accessibility Toggles (system-wide, persist across agents)
ToggleHotkeyWake WordMenu
Voice modeCtrl+Shift+V"start listening" / "stop listening"v
Braille outputCtrl+Shift+B-b
NeuralinkCtrl+Shift+N-n
Eye trackingCtrl+Shift+E-e
Voice agent select-"switch to lawclaw"s
Voice mode flow: Say "start listening" -> speak in any language -> system auto-detects, translates to English, processes through the current agent, translates response back, speaks it aloud. Say "stop listening" to deactivate.

What It Does
Legal Document Drafting
bash
lawclaw> /doc service agreement between ABC LLC and XYZ Corp for IT services - governing law Delaware
lawclaw> /translate the contract to German
Structured draft contract. German translation with legal terms preserved. Three-agent chain.

Clinical Triage + Hospital Routing
bash
mediclaw> /diagnose chest pain in Denver CO
Differential assessment, urgency triage, nearest ER with GPS coordinates.

3,800+ City Civic Database
bash
lawclaw> /jurisdiction Daytona Beach FL
Courts, Police, Jail, Hospitals (GPS), Library, Building Permits. Returns in under 0.05s from Chronicle FTS5.

Cross-Agent Mesh
bash
lawclaw> /plot bar sales data     # routes to plotclaw
lawclaw> /code python hello       # routes to claw_coder
Any agent accesses any capability. Circuit breaker protected.

Multilingual Voice Mode
bash
any agent> /voice
[VOICE] Listening... (speak "Necesito un documento legal")
# System detects Spanish, translates, processes, responds in Spanish aloud
Speak any language. System handles detection, translation, and response automatically.

Architecture
TierSystemsPurpose
Constitutional Closurelifecycle, enforcement, guarded_executor, execution_policyExecution safety
Cognitionchronicle_helper, procedural_memory, three_tierKnowledge retrieval
Intelligencesmart_router, agent_routerTask routing
Operationalvalidation, log_manager, shutdown, hooksOperations
Governancebudget, rate_limiter, error_handler, metrics, securityResource protection
Memory & Truthmemory_guard, source_registry, truth_resolver, decision_ledger, consensus, auditorKnowledge integrity
Infrastructureinput_handler, permissions, registry, config, routerSystem services
Telemetryobservability, chronicle_ledgerMonitoring
Accessibilityvoice_hook, io_adapter, status_barTTS/STT/Braille/Neuralink/Eye
Truth hierarchy: web_verified > chronicle > memory > inference. Lower-tier facts cannot override higher-tier sources.

LLM access: Sovereign Gateway only (shared/llm/client.py). Provider chain: Groq -> Ollama -> OpenRouter -> Anthropic.

Documentation
FilePurpose
CLAWPACK_ONBOARD.mdComplete system map + AI context
POWERSHELL_SURVIVAL_GUIDE.mdPowerShell environment rules
ARCHITECTURE.mdSystem design and data flow
AGENT_CAPABILITIES.mdCapability-to-agent registry
AGENT_TEMPLATE.mdBootstrap a new agent
BASEAGENT_GUIDE.mdMethods every agent inherits
CHRONICLE_GUIDE.mdShared knowledge database
CONSTITUTIONAL_COMPLIANCE_AUDIT.mdPer-agent compliance
shared/CONSTITUTION_v1.mdConstitutional law (frozen)
Known Active Work
AreaStatus
Chronicle recover_by_context19 call sites, non-blocking warnings
Capability routing7 partial agents
Enforcement engineDormant
Guarded executorDormant
Registry5 agents outside AGENT_REGISTRY dict
Benchmark Snapshot (2026-05-30)
MetricValue
Agent /help latency (median)0.2s
Civic command latency (Chronicle FTS5)0.03-0.28s
LLM inference (Groq)0.7s
LLM inference (Ollama)0.8s
Chronicle FTS5 entries35,553
Circuit breaker trips0
Lifecycle cleanup errors0
Voice commands deployed60 files, 21/21 agents
Data Licensing
Jurisdictional data, court records, building codes: CC BY 4.0 — See LICENSE_DATA
Software code: MIT License — See LICENSE
DOI: 10.5281/zenodo.19713157
