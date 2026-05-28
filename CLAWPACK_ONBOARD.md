> READ THIS FIRST. Do not write any code until you have read this entire document.

# CLAWPACK V2 - AI ONBOARDING CONTEXT

## What This Is
21-agent AI ecosystem. Menu-driven CLI. A2A routing on port 8766.
448MB Chronicle SQLite index at data/chronicle.db. Constitutional governance.
Built by Greg. You are helping build and maintain all 21 agents.

## Before You Write Any Code
1. Ask to see the current file if modifying an existing command.
2. Ask to see a working command if building a new stub.
3. Do not assume file contents - they may differ from conversation history.
4. State what you are about to do before doing it. One function at a time.

## How Commands Load
Commands in each agent's commands/ directory are loaded dynamically.
Each file needs: name = "/commandname" and def run(args): at module level.
No manual registration - just drop the .py file in the directory.

## Constitution (NON-NEGOTIABLE)
- All LLM access goes to Sovereign Gateway only (A2A to llmclaw). No direct API calls.
- All exceptions must log. except: pass is UNCONSTITUTIONAL.
- Truth hierarchy: web_verified > chronicle > memory > inference.
- Every agent has defined jurisdiction. No crossing.

## Empire-Wide Connection Layer (May 28, 2026)
All 21 agents import shared/_agent_helpers.py providing:
- log_err() - constitutional audit logging
- delegate() - cross-agent delegation to any agent
- llm() - Sovereign Gateway LLM calls
- chronicle() - Chronicle index search
- learn() - write to unified cross-agent memory
- recall_memory() - read from unified cross-agent memory

All 21 agents inherit from BaseAgent providing:
- call_agent() - cross-agent communication
- ask_llm() - Sovereign Gateway LLM
- smart_ask() - truth resolver pipeline
- search_chronicle() - 448MB indexed search
- learn_from_task() - shared learning (new)
- recall_prior() - memory recall (new)

## Shared Memory
All 23 lawclaw commands wired with _memory.py (show_prior + remember).
Cross-command learning via UnifiedMemory + MemoryGuard.
Confidence threshold: 0.75. Source types: web_verified, chronicle.
Proven working: /law "qualified immunity" showed 2 prior searches on second run.

## LawClaw Commands (all 23 complete, all memory-wired)

### Core Legal Research
- /docket - CourtListener API, real docket entries, jury demand, LLM summaries
- /law - Chronicle + CourtListener (SCOTUS + circuits), exact phrase search, authority ranking
- /cite - Citation parsing with concept router, Chronicle + WebClaw + LLM
- /precedent - Doctrine tracker by circuit, SCOTUS + circuits, cross-agent delegation
- /oral - CourtListener audio lookup, Chronicle + Oyez fallback, duration parsing
- /summarize - Universal legal input, structured briefs
- /statute - law.cornell.edu fetching, USC/UCC/FRCP/FRE/FRAP/state

### Court Systems
- /federal - Chronicle-first, filesystem-backed, circuits/SCOTUS/PACER/FRCP
- /state - State court lookup, 101 VA counties, fuzzy county matching
- /court - Filesystem jurisdiction lookup, .gov URL ranking

### Judicial & Civic Intelligence
- /judge - FJC biography + CourtListener positions + Chronicle
- /jurisdiction - 3,800+ cities, courts/police/jail/hospitals/libraries/permits
- /police - Police department lookup via jurisdiction files
- /detention - Jail/detention facility lookup
- /library - Library lookup with legal resource discovery
- /hospital - Hospital lookup with GPS coordinates

### Navigation & Utility
- /list - Jurisdiction database navigator (states/counties/cities)
- /browse - Display jurisdiction files, auto-open URLs
- /search - Local reference file search
- /analyze - Comprehensive legal text analysis
- /ask - AI law Q&A with Chronicle + WebClaw
- /brief - Case brief writer
- /stats - System statistics

## Patterns That Work
```python
# Shared memory (add to any command)
from agents.lawclaw.commands._memory import show_prior, remember
prior = show_prior(args, out)  # at start
remember(command="/name", query=args, result_summary=result[:400], ...)  # at end

# Empire-wide helpers (any agent)
from shared._agent_helpers import delegate, llm, chronicle, log_err, learn, recall_memory
Forbidden (DO NOT DO)
import anthropic or any direct LLM provider import

requests.get() in commands (use webclaw via A2A)

Hardcoded lookup dicts when data exists in Chronicle

Silent exception handling (log everything)

Known Issues
CourtListener rate limits (429) on rapid queries - 125 requests/day

URL noise in /federal from unrelated Chronicle hits

SDNY judges page is JS-rendered

/oral CourtListener audio database is sparse

Key Files
a2a_server.py - port 8766

shared/_agent_helpers.py - empire-wide utilities (all 21 agents)

shared/base_agent.py - BaseAgent foundation

shared/memory/unified_memory.py - cross-agent knowledge store

agents/lawclaw/commands/_helpers.py - lawclaw shared utilities

agents/lawclaw/commands/_memory.py - shared memory bridge

agents/webclaw/references/lawclaw/jurisdictions/us/ - 3,800+ cities

Architecture Docs
A2A_PROTOCOL.md - how agents call each other

SHARED_MEMORY_PROTOCOL.md - how agents learn together

AGENT_CAPABILITIES.md - who does what

BASEAGENT_GUIDE.md - what BaseAgent provides

CHRONICLE_GUIDE.md - data layer

Session Log
2026-05-27: All 12 lawclaw commands built. 4 civic commands added.
_helpers.py and _memory.py created.

2026-05-28: All 21 agents wired with shared/_agent_helpers.py.
All 23 lawclaw commands wired with shared memory (show_prior + remember).
Shared learning pipeline proven with /law (2 prior searches surfaced).
Exact phrase search + authority ranking in /law.
base_agent.py: learn_from_task() and recall_prior() added.
Root documentation cleaned up.
Cross-agent delegation available empire-wide.
