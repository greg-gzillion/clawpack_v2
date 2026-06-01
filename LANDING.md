# Clawpack V2 ? What Is This?

A local-first multi-agent AI operating system. 21 specialized agents communicate
through a central message bus, governed by a frozen Constitution. No cloud required.

## In Plain Terms

You type /court Georgetown CO and it searches through 3,800+ city jurisdiction
files, finds the municipal court data for Georgetown (in Clear Creek County),
and returns addresses, phone numbers, and websites ? in about 500ms.

You type /jurisdiction Miami FL and it returns courts, police, jails, hospitals,
libraries, and building permits for Miami-Dade County.

You say "court Denver Colorado" and voice recognition routes it through the same
pipeline. Cross-agent delegation means the legal agent can call the document agent
to generate a formatted PDF, or the chart agent to visualize data.

## Quick Start

`ash
# 1. Install Ollama and pull a model
ollama pull deepseek-r1:8b

# 2. Start the server
python a2a_server.py

# 3. Launch the menu
python clawpack.py

# 4. Try a command
lawclaw> /court Georgetown CO
lawclaw> /jurisdiction Miami FL
Architecture (Three Layers)
Layer 1: A2A Server (port 8766) ? Central message bus. Every agent registers here.
Every inter-agent communication routes through here. Circuit breaker protected.

Layer 2: Shared Infrastructure (93 modules) ? Constitutional enforcement,
truth consensus scoring, memory guard (blocks hallucination persistence),
budget controller, rate limiter, structured logging, event bus.

Layer 3: 21 Specialized Agents ? Each with defined jurisdiction:
lawclaw (legal), mediclaw (medical), claw_coder (code), plotclaw (charts),
docuclaw (documents), webclaw (search), dreamclaw (AI vision), and 14 more.

All agents inherit from BaseAgent which provides call_agent(), ask_llm(),
search_chronicle() (448MB SQLite FTS5), and lookup_jurisdiction().

What Makes It Different
Constitutional governance. The Constitution (shared/CONSTITUTION_v1.md) is
frozen law. Enforcement engine blocks forbidden operations before execution.
Truth hierarchy: web_verified > chronicle > memory > inference.

Local-first. Runs on your machine. Ollama for local inference. No API keys
required. Sovereign Gateway manages provider fallback: Groq -> Ollama ->
OpenRouter -> Anthropic.

Jurisdiction dataset. 3,800+ US cities across all 50 states, organized by
county, with municipal courts, police, jails, hospitals, libraries, and
building permits. 41,286 indexed reference files (88MB).

Cross-agent delegation. No agent works alone. LawClaw enriches with
jurisdiction data before delegating to DocuClaw. MedicLaw routes to WebClaw
for latest research. Any agent can call any capability via the registry.

Accessibility layer. Voice control (speech-to-text with automatic / prefix
detection), Braille output, TTS, language translation (42 languages),
Neuralink/eye tracking stubs.

Limitations (Honest)
Voice accuracy. The desktop Python voice loop uses speech_recognition
which is limited. The PWA (mobile/) uses native Web Speech API ? much better.
Desktop voice is dev tooling; phone PWA is the production voice interface.

LLM speed. Local inference on CPU is slow. deepseek-r1:8b takes 30-120s
for complex queries. gemma3:4b is faster. Groq cloud API is instant when
available (free tier, rate-limited).

Memory recall. The cross-session memory system remembers past searches
but doesn't filter by location yet. A search for "court Colorado" may surface
old Virginia results. Being fixed.

Jurisdiction coverage. Some cities are missing (Greeley CO under Weld County,
for example). The dataset structure is correct ? it just needs population.

Files That Matter
FileWhat It Is
a2a_server.pyStart this first. The message bus.
clawpack.pyThe menu. Launch agents from here.
shared/base_agent.pyWhat every agent inherits.
shared/llm/client.pySovereign Gateway. All LLM access here.
shared/CONSTITUTION_v1.mdSupreme law. Frozen.
agents/lawclaw/Reference implementation. Start here to understand agents.
agents/webclaw/references/lawclaw/jurisdictions/us/3,800+ city jurisdiction files.
data/chronicle.db448MB SQLite FTS5 shared knowledge index.
CLAWPACK_ONBOARD.mdFull system map + AI context.
ARCHITECTURE.mdSystem design and data flow.
docs/QUICKSTART.mdStep-by-step setup.
Current State (June 1, 2026)
Working: All 21 agents responsive. Court resolver fixed (city-first traversal).
Voice pipeline functional (speech->transcribe->prefix->A2A->response).
Enforcement gate active. Rate limiter active. Structured logging. Event bus.

Being fixed: Memory jurisdiction filtering. Ledger corruption. Command loading scope.
Missing cities in dataset.

Who This Is For
Developers interested in local sovereign AI, multi-agent systems, legal research
automation, or constitutional AI enforcement. Not a commercial product. A working
research system that demonstrates what's possible when agents have defined
jurisdictions, shared memory, and constitutional boundaries.
