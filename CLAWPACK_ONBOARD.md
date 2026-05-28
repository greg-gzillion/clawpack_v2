> READ THIS FIRST. Do not write any code until you have read this entire document.

# CLAWPACK V2 - AI ONBOARDING CONTEXT

## What This Is
21-agent AI ecosystem. Menu-driven CLI. A2A routing on port 8766.
448MB Chronicle SQLite index at data/chronicle.db. Constitutional governance.
Built by Greg. You are helping build and maintain lawclaw commands.

## Before You Write Any Code
1. Ask to see the current file if modifying an existing command.
2. Ask to see a working command (e.g. docket.py or jurisdiction.py) if building a new stub.
3. Do not assume file contents - they may differ from what is in conversation history.
4. State what you are about to do before doing it. One function at a time.

## How Commands Load
Commands in agents/lawclaw/commands/ are loaded dynamically by __init__.py.
Each file needs: name = "/commandname" and def run(args): at module level.
No manual registration - just drop the .py file in the directory.

## Constitution (NON-NEGOTIABLE)
- All LLM access goes to Sovereign Gateway only (A2A to llmclaw). No direct API calls.
- All exceptions must log. except: pass is UNCONSTITUTIONAL.
- Truth hierarchy: web_verified > chronicle > memory > inference.
- Every agent has defined jurisdiction. No crossing.

## Correct Exception Handling
```python
# WRONG - unconstitutional
except:
    pass

# CORRECT
except Exception as e:
    log_err("agent_name", "context", str(e)[:200])
Working Commands (all 12 lawclaw commands complete)
/docket
CourtListener API. Real docket entries from recap_documents. Paginated entry fetch.
Jury demand detection. LLM timeline summaries. Multi-court disambiguation.

/court
Filesystem jurisdiction lookup. State/county/city matching. URL ranking with .gov preference.

/cite
Citation parsing with concept router. Chronicle search + WebClaw fetch + LLM analysis.

/federal
Chronicle-first, filesystem-backed. NO HARDCODED DICTS.
Circuits, SCOTUS, PACER, FRCP, city lookups.
SDNY judges: page is JS-rendered. Honest fallback in place - NOT a bug, do not fix.

/judge
FJC biography (primary) + CourtListener positions (supplemental) + Chronicle.
Anti-repetition prompt. Last-name search. Case hallucination guard.

/jurisdiction
Chronicle + filesystem civic intelligence. City and county lookup.
Courts, police, jail, hospitals with GPS coordinates, library, building permits.
3,800+ cities indexed. County-level court files + city-level civic files.

/law
Chronicle + CourtListener federal opinions (SCOTUS + circuits).
Topic-based research with real citations. /docket chain ready.

/oral
CourtListener docket search + audio lookup (two-step pipeline).
SCOTUS + circuit court filter. Oyez.org fallback. Duration parsing.

/precedent
Doctrine tracker by circuit. SCOTUS + circuit court case search.
Controlling authority, circuit splits, trend direction. Cross-agent delegation offers.

/state
State court lookup via jurisdiction files. County list + court details.
101 VA counties working. Fuzzy matching for misspelled counties.

/statute
Statute lookup via law.cornell.edu + Chronicle + LLM.
USC, UCC, FRCP, FRE, FRAP, state statutes. Real statutory text fetching.

/summarize
Universal legal input summarizer. Case names, docket URLs, statutes, text.
Structured summary: overview, facts, issue, holding, reasoning, significance.

Civic Commands
/police - Police department lookup via jurisdiction files
/detention - Jail/detention facility lookup via jurisdiction files
/library - Library lookup with legal resource discovery
/hospital - Hospital lookup with GPS coordinates

Shared Memory (_memory.py)
Cross-command learning via UnifiedMemory + MemoryGuard.
Confidence threshold: 0.75. Source types: web_verified, chronicle.
Wired into: /oral, /law, /precedent, /list.

Empire-Wide Connection Layer
All 21 agents now import shared/_agent_helpers.py for:

log_err() - constitutional audit logging

delegate() - cross-agent delegation to any agent

llm() - Sovereign Gateway LLM calls

chronicle() - Chronicle index search

Patterns That Work
python
# LLM via A2A
resp = requests.post(f"{A2A}/v1/message/llmclaw",
    json={"task": f"/llm {prompt}", "agent": "lawclaw"}, timeout=120)

# WebClaw fetch via A2A
resp = requests.post(f"{A2A}/v1/message/webclaw",
    json={"task": f"fetch {url}", "agent": "lawclaw"}, timeout=20)

# Chronicle search (448MB SQLite index)
from agents.webclaw.core.chronicle_ledger import get_chronicle
c = get_chronicle()
results = c.recover_by_context("query", limit=10)

# Filesystem jurisdiction search
LAW_REFS = Path(__file__).parent.parent.parent.parent / "agents" / "webclaw" / "references" / "lawclaw"
for md_file in (LAW_REFS / "jurisdictions" / "us").rglob("*.md"):
    content = md_file.read_text(encoding='utf-8', errors='ignore')

# CourtListener API (token from .env)
GET {COURTLISTENER_API}/search/?q=term&type=o&order_by=score desc
GET {COURTLISTENER_API}/dockets/?docket_number=X

# Shared memory
from agents.lawclaw.commands._memory import recall, remember, show_prior

# Empire-wide helpers (any agent)
from shared._agent_helpers import delegate, llm, chronicle, log_err
Forbidden (DO NOT DO)
import anthropic or any direct LLM provider import

requests.get() in lawclaw commands (use webclaw via A2A)

Hardcoded lookup dicts when data exists in Chronicle

Silent exception handling (log everything)

DeepSeek will suggest requests.get() fallbacks when webclaw fails. Reject this.

Known Issues
URL noise in /federal results from unrelated Chronicle hits

SDNY judges page is JS-rendered

CourtListener rate limits (429) on rapid queries

/oral CourtListener audio database is sparse - Oyez fallback handles this

Key Files
a2a_server.py - port 8766

shared/_agent_helpers.py - empire-wide agent utilities (all 21 agents import)

shared/base_agent.py - BaseAgent foundation class

shared/llm/client.py - Sovereign Gateway

shared/memory/unified_memory.py - UnifiedMemory

shared/memory_guard.py - MemoryGuard (0.75 threshold)

agents/lawclaw/commands/ - all lawclaw commands

agents/lawclaw/commands/_helpers.py - lawclaw shared utilities

agents/lawclaw/commands/_memory.py - shared memory helper

agents/webclaw/core/chronicle_ledger.py - Chronicle interface

agents/webclaw/references/lawclaw/jurisdictions/us/ - all jurisdiction data

.env - API tokens

Architecture Docs (read these)
A2A_PROTOCOL.md - how agents call each other

SHARED_MEMORY_PROTOCOL.md - how agents learn together

AGENT_CAPABILITIES.md - who does what, connection status

BASEAGENT_GUIDE.md - what BaseAgent provides

CHRONICLE_GUIDE.md - data layer guide

Session Log
2026-05-27: All 12 lawclaw commands built and working. 4 civic commands added.
_helpers.py created for shared command utilities.
_memory.py created for cross-command shared learning.

2026-05-28: All 21 agents wired with shared/_agent_helpers.py (log_err, delegate).
Cross-agent delegation available empire-wide.
Root documentation cleaned up and organized.
All stub commands completed (/state, /statute, /precedent, /summarize).
Civic commands added (/police, /detention, /library, /hospital).
