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

## Constitutional Command Lifecycle (EFFECTIVE MAY 28, 2026)

**Every command MUST participate in the constitutional runtime.**
A command is not a standalone function — it is a lifecycle participant.

### Required Lifecycle Phases
Every command's `run(args)` MUST execute these phases:

1. **RECALL** — show_prior(args, out) at start
2. **REASON** — LLM via _helpers.llm() or chronicle/webclaw fetch
3. **OUTPUT** — return formatted result string
4. **MEMORY WRITE** — remember() after successful result
5. **DELEGATION SURFACE** — auto_delegate() offers in output
6. **LEARNING** — learn_fact() after LLM synthesis

### Automatic Enforcement (May 29, 2026)
**The handler boundary enforces phases 4-8 automatically.** No per-command edits needed.
Every command that passes through `LawClawHandler.handle()` gets:
- Budget check (shared/llm/budget.py)
- Rate limiting (shared/rate_limiter.py)
- Memory write (unified_memory.py)
- Learning extraction (shared/_agent_helpers.py)
- Audit ledger (shared/decision_ledger.py)
- Consensus scoring (shared/consensus_engine.py)
- Chronicle audit log (shared/llm/auditor.py)

### What Each Phase Connects To
| Phase | Function | Shared Module | Constitutional Article |
|-------|----------|---------------|----------------------|
| RECALL | show_prior() | unified_memory.py | Article VI Section 1 |
| REASON | llm() / smart_llm() | llm/client.py (Sovereign Gateway) | Article I Section 1 |
| MEMORY | remember() | memory_guard.py → unified_memory.py | Article VI Section 2 |
| LEARNING | learn_fact() | base_agent.py → unified_memory.py | Article VI Section 1 |
| DELEGATION | auto_delegate() | registry.py → call_agent() | Article III Section 2 |

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
All 24 lawclaw commands wired with _memory.py (show_prior + remember).
Cross-command learning via UnifiedMemory + MemoryGuard.
Confidence threshold: 0.75. Source types: web_verified, chronicle.
Proven working: /law "qualified immunity" showed 3 prior searches on second run.

## LawClaw Commands (all 24 complete, all memory-wired)

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

### Document Generation & Correction
- /doc - Generate court-specific legal documents via docuclaw with jurisdiction data
- /draft - Alias for /doc
- /correct - Community correction of facts/URLs via consensus engine

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

# Constitutional lifecycle (EVERY command must include)
from agents.lawclaw.commands._helpers import auto_delegate
auto_delegate(result, urls, out)  # offer cross-agent actions in output
Forbidden (DO NOT DO)
import anthropic or any direct LLM provider import

requests.get() in commands (use webclaw via A2A)

Hardcoded lookup dicts when data exists in Chronicle

Silent exception handling (log everything)

Building a command that returns output but does NOT write to memory or surface delegation

Known Issues
CourtListener rate limits (429) on rapid queries - 125 requests/day

URL noise in /federal from unrelated Chronicle hits

SDNY judges page is JS-rendered

/oral CourtListener audio database is sparse

Constitutional Source Validation shows CONFLICT for legal citation numbers (false positive)

Key Files
a2a_server.py - port 8766

shared/_agent_helpers.py - empire-wide utilities (all 21 agents)

shared/base_agent.py - BaseAgent foundation

shared/memory/unified_memory.py - cross-agent knowledge store

shared/memory_guard.py - confidence threshold enforcement

shared/truth_resolver.py - source conflict resolution

shared/decision_ledger.py - tamper-evident audit chain

shared/guarded_executor.py - dangerous operation gateway

shared/enforcement/engine.py - pre/post execution gates

shared/consensus_engine.py - reputation-based truth scoring

shared/court_rules_schema.py - canonical court filing rules format

shared/source_registry.py - trust scores for 40+ sources

shared/constitutional_command.py - decorator specification

agents/lawclaw/commands/_helpers.py - lawclaw shared utilities

agents/lawclaw/commands/_memory.py - shared memory bridge

agents/lawclaw/core/court_rules_extractor.py - live court rules extraction

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
Constitutional Command Lifecycle section added — every command MUST participate in all 6 phases.
First constitutional cross-agent flow: /jurisdiction → remember_court() → /draft → recall_court() → call_agent("docuclaw").

2026-05-29: Constitutional execution boundary activated — budget, rate limit, memory, learning,
audit trail, consensus, and auditor fire automatically for all commands via handler injection.
Consensus truth engine deployed with structured claim extraction (citation:, concept:, source_url:).
/correct command for self-healing URL/fact corrections with anti-pattern learning.
Court rules extractor built — reads 3,800-city jurisdiction files, fetches live court websites,
extracts structured filing requirements via LLM, caches to Chronicle.
/doc command generates jurisdiction-specific legal documents via docuclaw with full court data.
Source registry fixed — .gov domains at 0.92 authoritative, .us court domains at 0.85 verified.
Truth resolver patched — .gov wildcard returns web_verified classification.
Location extraction fixed for structured args (handles "- plaintiff: John Smith" format).
Proven: /doc motion to dismiss Miami FL - plaintiff: John Smith - defendant: ABC Corp
produced properly captioned motion with Florida Rule 1.140(b)(6), correct court, authoritative sources.
Total commands: 24. Total shared modules actively used: 15. Constitutional runtime: ACTIVE.