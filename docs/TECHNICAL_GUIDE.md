# Clawpack V2 ? Technical Guide

## Architecture

Three-layer multi-agent runtime. All layers communicate through HTTP on localhost.

### Layer 1: A2A Server (2a_server.py, port 8766)

Central message bus. ThreadingHTTPServer. Every agent registers at startup.
POST /v1/message/{agent} ? Send task to agent
GET /health ? Server health + memory stats
GET /v1/agents ? List all 21 agents
GET /metrics ? Per-agent request counters

text

Circuit breaker on all cross-agent calls: 5 consecutive failures opens circuit
for 60 seconds. Half-open state allows 3 test calls before closing.

### Layer 2: Shared Infrastructure (shared/, 93 modules)

Every module is importable by any agent. No agent owns infrastructure.

**Constitutional Closure**
- lifecycle.py ? Guaranteed cleanup after every agent invocation. GC, Chronicle write, ledger record. Wrapped around every A2A request. 0 errors.
- enforcement/engine.py ? Pre-execution gate active. Scans tasks for 19 forbidden patterns before dispatch.
- guarded_executor.py ? Only legal path for file deletion, git operations, subprocess execution. All blocked by default.
- execution_policy.py ? Hard boundaries enum. ALLOW_DELETE = False, ALLOW_GIT_FORCE_PUSH = BLOCKED.

**Memory & Truth**
- memory_guard.py ? Inference-tier facts NEVER persist. Confidence below 0.75 blocked. Only web_verified and chronicle sources may write.
- consensus_engine.py ? Reputation-based truth scoring. Formula: (source_trust ? 0.35) + (consensus_count ? 0.25) + (recency ? 0.15) + (verification_count ? 0.15) + (cross_agent_agreement ? 0.10).
- 	ruth_resolver.py ? Multi-source conflict resolution by priority, not consensus.
- source_registry.py ? .gov domains at 0.92 trust, .us courts at 0.85.
- decision_ledger.py ? Immutable hash-chained audit trail. erify_integrity() validates entire chain.

**Governance**
- llm/budget.py ? Per-agent daily limits. Global budget: /day. lawclaw: , claw_coder: , webclaw: .
- ate_limiter.py ? Per-minute and per-day request throttling.
- error_handler.py ? Exponential backoff with jitter, retry classification, dead letter queue.

**Accessibility** (unified in ccessibility.py)
- TTS via pyttsx3, STT via speech_recognition with USB mic preference
- Wake words: "start listening" / "stop listening", auto-sleep after 2min
- Voice commands: flexible detection anywhere in utterance, / prefix auto-add
- State name ? code mapping (Nevada ? NV), natural language ? command mapping
- Braille Unicode output, language detection (6 languages), translation via LLM
- Neuralink/eye tracker stubs via io_adapter.py

**Event Bus** (event_bus.py)
- Canonical input pathway. CommandEvent dataclass with EventSource and EventIntent enums.
- Queue-based cross-thread delivery. Voice loop pushes, menu and agent loops poll.
- Sources: keyboard, voice, API, system, accessibility
- Intents: switch_agent, launch_agent, run_command, toggle_voice, sleep_voice, wake_voice, system_quit

### Layer 3: Agents (gents/, 21 agents)

**Domain Specialists**
| # | Agent | Domain | Key Commands |
|---|-------|--------|-------------|
| 1 | lawclaw | Legal research | /court, /jurisdiction, /law, /cite, /statute, /docket, /doc |
| 4 | mathematicaclaw | Math & computation | /math, /solve, /derivative, /integral, /plot |
| 7 | interpretclaw | Translation (42 languages) | /translate, /detect, /speak |
| 8 | langclaw | Language teaching | /lesson, /vocab, /practice, /teach |
| 9 | claw_coder | Code generation (39 languages) | /code, /explain, /debug, /review, /tutorial |
| 14 | mediclaw | Medical analysis | /diagnose, /treatment, /emergency, /er |
| 15 | dreamclaw | AI vision | /dream, /imagine |
| 16 | designclaw | Graphic design | /brand, /logo, /colors, /kit |
| 17 | draftclaw | Technical drawings | /blueprint, /permit, /structural, /cad |
| 18 | crustyclaw | Rust specialist | /rust, /audit, /pinch, /fix |
| 20 | drawclaw | AI drawing | /draw, /paint, /sketch, /illustrate |

**System Utilities**
| # | Agent | Domain | Key Commands |
|---|-------|--------|-------------|
| 2 | flowclaw | Diagrams & flowcharts | /flowchart, /mindmap, /sequence, /architecture |
| 3 | docuclaw | Document creation | /create, /export, /letter, /report (31 commands) |
| 10 | dataclaw | Data processing | /search, /find, /export |
| 11 | webclaw | Web search & Chronicle | search, fetch, /chronicle |
| 12 | fileclaw | File operations | /import, /export, /convert |
| 13 | plotclaw | Charts & graphs | /bar, /pie, /scatter, /hist (15 chart types) |
| 19 | rustypycraw | Code analysis | /crawl, /scan, /analyze |

**System Infrastructure**
| # | Agent | Domain | Key Commands |
|---|-------|--------|-------------|
| 5 | liberateclaw | Model liberation | /liberate, /obliterate, /models |
| 6 | txclaw | Blockchain | /tx, /network, /contract |
| 21 | llmclaw | Model management | /llm, /use, /list, /models |

## Agent Anatomy

Each agent follows the same structure:
agents/lawclaw/
??? agent_handler.py # Inherits BaseAgent, dispatches commands
??? commands/ # Individual command files
? ??? _memory.py # Cross-session memory bridge
? ??? _helpers.py # Domain-specific utilities (CourtListener API, etc.)
? ??? court.py # name = "/court", def run(args, agent=None)
? ??? ... # 33 commands total for lawclaw

text

Command files need only:
`python
name = "/commandname"
def run(args, agent=None):
    # agent.search_chronicle() ? 448MB FTS5 index
    # agent.ask_llm() ? Sovereign Gateway
    # agent.call_agent() ? cross-agent delegation with circuit breaker
    # agent.lookup_jurisdiction() ? civic data (0.03-0.28s)
    return "result string"
No registration required. Loaded dynamically by the handler at startup.

Provider Chain (Sovereign Gateway)
All LLM access routes exclusively through shared/llm/client.py.
No agent imports LLM libraries directly. Constitutional Article I.

text
User prompt ? BaseAgent.ask_llm()
    ? shared/llm/client.py (Sovereign Gateway)
        ? Budget check (per-agent daily limit)
        ? Provider chain (auto-detected order):
            1. Groq (llama-3.3-70b-versatile, free tier, 0.7s)
            2. Ollama (model from active_model.json, local, free)
            3. OpenRouter (google/gemma-4-26b-a4b-it:free, free tier)
            4. Anthropic (claude-haiku-4-5-20251001, paid)
        ? Automatic fallback on failure
        ? Chronicle audit log
        ? Budget record
    ? Response
Switch models at runtime: llmclaw> /use gemma3:4b

Data Layer
Chronicle (data/chronicle.db)
SQLite FTS5, 448MB, 35,000+ interactions. Contains indexed full-text of
all reference files across all agents. Every agent queries the same Chronicle.

text
BaseAgent.search_chronicle(query, limit=10) ? FTS5 search ? list of dicts
BaseAgent.lookup_jurisdiction("Denver CO", "hospital") ? FTS5 ? structured dict
Jurisdiction Dataset
text
agents/webclaw/references/lawclaw/jurisdictions/us/{ST}/
??? {County}/
    ??? building_code.md
    ??? county_court.md
    ??? district_court.md
    ??? family_court.md
    ??? {City}/
        ??? municipal_court.md
        ??? law_resources.md
        ??? building_code.md
41,286 indexed reference files, 88MB. Organized state ? county ? city.
The /court resolver does city-first traversal: searches all counties
for matching city folder, falls back to county, then state.

Memory System
UnifiedMemory ? cross-agent fact storage with keyword index

memory_guard ? blocks inference-tier facts, enforces confidence ? 0.75

Only web_verified and chronicle sources may persist to memory

Memory staleness warnings on facts older than 24 hours

Constitutional Enforcement
The Constitution (shared/CONSTITUTION_v1.md) is frozen law. Key principles:

Article I ? All LLM access through Sovereign Gateway only

Article II ? Each agent has defined jurisdiction. No crossing.

Article III ? Delegate before expanding. Use call_agent().

Article V ? Truth hierarchy: web_verified > chronicle > memory > inference

Article VII ? except: pass is UNCONSTITUTIONAL

Article XI ? Enforcement engine pre/post execution gates

Enforcement engine scans every A2A request against 19 forbidden patterns
before agent dispatch. Currently non-blocking during activation phase.

Cross-Agent Communication
Three paths:

Capability Registry ? unrecognized commands auto-route to correct agent via shared/capabilities.py

Direct Delegation ? agent.call_agent("docuclaw", task, timeout=60)

Enriched Delegation ? domain expertise added before forwarding (lawclaw ? docuclaw with court context)

Every cross-agent call is circuit breaker protected and budget enforced.

Voice Pipeline
text
Microphone ? speech_recognition ? text ? intent detection
    ? known command check (anywhere in utterance)
    ? / prefix auto-add
    ? state name ? code mapping (Nevada ? NV)
    ? natural language ? command mapping (contract ? /doc)
    ? event_bus.push_event()
    ? A2A POST /v1/message/{agent}
    ? agent handler ? command execution ? response
Flexible detection finds command words anywhere in the utterance:
"Las Vegas Court Nevada" ? /court las vegas NV

API Keys
Configured in .env:

text
GROQ_API_KEY=           # Free tier, 0.7s latency
ANTHROPIC_API_KEY=      # Paid, 1.2s latency
OPENROUTER_API_KEY=     # Free tier available
COURTLISTENER_API_KEY=  # Legal research API
None required for basic operation. Ollama provides fully offline capability.

Ports
PortService
8766A2A server (agent communication)
11434Ollama API (local LLM inference)
Quick Reference
python
# From any agent handler or command:
agent.ask_llm(prompt)                    # Sovereign Gateway
agent.call_agent("docuclaw", task)       # Cross-agent delegation
agent.search_chronicle(query, limit=10)  # 448MB FTS5
agent.lookup_jurisdiction("Denver CO")   # Civic data, 0.03s
agent.cached_search(query)              # Web search, 24hr cache
agent.search_web(query)                 # Live web search
agent.learn(key, value)                 # Persist to memory
agent.recall(key)                       # Retrieve from memory

# From any command file:
from shared._agent_helpers import llm, chronicle, web, delegate, log_err
from shared.event_bus import push_event, get_event, EventIntent
from shared.accessibility import speak, listen, toggle_voice, status
