# Clawpack V2

A local multi-agent AI runtime. 21 specialized agents communicate through a
central message bus with constitutional governance. Runs on your machine.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19713157.svg)](https://doi.org/10.5281/zenodo.19713157)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)

**21 agents ? 90+ shared systems ? Chronicle FTS5 (35K+) ? A2A routing ? Voice/STT/TTS/Braille**

---

## Why Clawpack Exists

Most AI tools are single-model chatbots behind API paywalls. Clawpack is
different: 21 agents with defined jurisdictions, cross-agent delegation,
voice/braille/translation accessibility, and constitutional governance.
Runs locally with Ollama. Also works with Groq, Anthropic, and OpenRouter.

---

## Runtime Health

| Metric | Value |
|--------|-------|
| Agent availability | 21/21 responsive |
| A2A transport | Healthy (port 8766) |
| Chronicle index | 35,553 interactions |
| LLM providers | 4/4 operational |
| Provider chain | Groq -> Ollama -> OpenRouter -> Anthropic |
| Lifecycle cleanup errors | 0 |
| Voice/listen/translate/braille | 21/21 agents |

---

## See It In Action

`ash
# One command
python run.py

# Then try:
lawclaw> /court Denver CO           # Court lookup with real data
lawclaw> /translate contract to German # Legal term preservation
mediclaw> /diagnose chest pain      # Medical triage
lawclaw> /plot bar sales data       # Auto-routes to PlotClaw
Quick Start
bash
# Install Ollama and pull a model
ollama pull gemma3:4b

# Install dependencies
pip install -r requirements.txt

# Terminal 1: Start the server
python a2a_server.py

# Terminal 2: Launch the menu
python clawpack.py
Type 1 for the legal agent. Try /court Denver CO or /help.

Architecture
TierSystemsPurpose
Constitutional Closurelifecycle, enforcement, guarded_executor, execution_policyExecution safety
Cognitionchronicle_helper, procedural_memory, three_tierKnowledge retrieval
Intelligencesmart_router, agent_routerTask routing
Operationalvalidation, log_manager, shutdown, hooksOperations
Governancebudget, rate_limiter, error_handler, metrics, securityResource protection
Memory & Truthmemory_guard, source_registry, truth_resolver, decision_ledger, consensusKnowledge integrity
Infrastructureinput_handler, permissions, registry, config, router, event_busSystem services
Telemetryobservability, chronicle_ledgerMonitoring
Accessibilityaccessibility.py (unified), speech.py, locale.pyVoice, TTS, STT, Braille
Truth hierarchy: web_verified > chronicle > memory > inference.
Lower-tier facts cannot override higher-tier sources.

LLM access: Sovereign Gateway only (shared/llm/client.py).
No agent imports LLM libraries directly.

The Agents
Domain Specialists
#AgentDomain
1lawclawLegal research, court lookup, case law
4mathematicaclawMath, calculus, equations
7interpretclawTranslation (42 languages)
8langclawLanguage teaching
9claw_coderCode generation (39 languages)
14mediclawMedical analysis, hospital lookup
15dreamclawAI vision and generation
16designclawGraphic design, logos
17draftclawTechnical drawings, blueprints
18crustyclawRust programming specialist
20drawclawAI drawing and art
System Utilities
#AgentDomain
2flowclawDiagrams, flowcharts, mindmaps
3docuclawDocument creation, PDF export
10dataclawData processing, local search
11webclawWeb search, Chronicle indexing
12fileclawFile operations, format conversion
13plotclawCharts and graphs
19rustypycrawCode analysis and crawling
System Infrastructure
#AgentDomain
5liberateclawModel liberation and management
6txclawBlockchain transactions
21llmclawModel selection, Sovereign Gateway
Honest Limitations
Voice accuracy: Desktop Python STT is limited. The PWA (mobile/) uses
native Web Speech API and is significantly better. Desktop voice is dev tooling.

LLM speed: Local inference on CPU is slow. GPU helps substantially.
Groq cloud API is fast when available (free tier, rate-limited).

Jurisdiction coverage: Not all cities are populated. Some states are
incomplete. The county?city hierarchy is correct ? needs population.

Memory recall: Past searches can surface irrelevant results because the
keyword index doesn't filter by geographic location. Being fixed.

Enforcement engine: Logs constitutional violations but doesn't block them
yet. Switch from warn-only to enforce is pending.

Documentation
FilePurpose
LANDING.mdQuick overview for new visitors
docs/BEGINNERS_GUIDE.mdStep-by-step for non-developers
docs/TECHNICAL_GUIDE.mdArchitecture, agent anatomy, API reference
CLAWPACK_ONBOARD.mdFull system map + AI agent context
ARCHITECTURE.mdSystem design and data flow
AGENT_CAPABILITIES.mdWhat each agent can do
CHRONICLE_GUIDE.mdShared knowledge database
shared/CONSTITUTION_v1.mdConstitutional law (frozen)
License
Code: MIT. Jurisdictional data: CC BY 4.0.
DOI: 10.5281/zenodo.19713157
