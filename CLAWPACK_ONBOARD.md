> READ THIS FIRST. Do not write any code until you have read this entire document.

# CLAWPACK V2 — AI ONBOARDING CONTEXT

## What This Is
21-agent AI ecosystem. Menu-driven CLI. A2A routing on port 8766.
448MB Chronicle SQLite index at data/chronicle.db. Constitutional governance.
Built by Greg. You are helping build and maintain lawclaw commands.

## Before You Write Any Code
1. Ask to see the current file if modifying an existing command.
2. Ask to see a working command (e.g. docket.py or jurisdiction.py) if building a new stub.
3. Do not assume file contents — they may differ from what's in conversation history.
4. State what you're about to do before doing it. One function at a time.

## How Commands Load
Commands in `agents/lawclaw/commands/` are loaded dynamically by `__init__.py`.
Each file needs: `name = "/commandname"` and `def run(args):` at module level.
No manual registration — just drop the .py file in the directory.

## Constitution (NON-NEGOTIABLE)
- All LLM access → Sovereign Gateway only (A2A → llmclaw). No direct API calls.
- All exceptions must log. `except: pass` is UNCONSTITUTIONAL.
- Truth hierarchy: web_verified > chronicle > memory > inference.
- Every agent has defined jurisdiction. No crossing.

## Correct Exception Handling
```python
# WRONG — unconstitutional
except:
    pass

# CORRECT
except requests.exceptions.Timeout:
    _log("lawclaw", "command_timeout", str(e)[:100])
except Exception as e:
    _log("lawclaw", "command_error", str(e)[:200])
Working Commands
/docket
CourtListener API. Real docket entries from recap_documents. Paginated entry fetch.
Jury demand detection. LLM timeline summaries. Multi-court disambiguation.
Working: case number search, CourtListener URL drill-down. ✓

/court
Filesystem jurisdiction lookup. State/county/city matching. URL ranking with .gov preference.
Excludes non-legal civic files. LLM synthesis of court info.
Working: all states, counties, cities with jurisdiction files. ✓

/cite
Citation parsing with concept router. Chronicle search for reference data.
WebClaw fetch for live sources. LLM citation analysis with retry and fallback.
Working: statutes, case law, UCC, federal rules. ✓

/federal
Chronicle-first, filesystem-backed. NO HARDCODED DICTS.
Uses chronicle_search(), search_jurisdiction_files(), cl_get(), webclaw_fetch().
Working: circuits, SCOTUS, PACER, FRCP, city lookups (Bedford VA).
SDNY judges: page is JS-rendered. WebClaw returns metadata only. Honest fallback in place — NOT a bug, don't "fix" it. ✓

/judge
FJC biography (primary) + CourtListener positions (supplemental) + Chronicle.
Anti-repetition prompt. Last-name search for better CourtListener coverage.
Case hallucination guard. Working: Sotomayor, Pitman.
Note: CourtListener /people/ is sparse — FJC is primary source. ✓

/jurisdiction
Chronicle + filesystem civic intelligence. City and county lookup.
Courts, police, jail, hospitals with GPS coordinates, library, building permits.
3,800+ cities indexed. County-level court files + city-level civic files.
Per-file truncation to prevent LLM timeout. Working: Bedford VA, Daytona Beach FL,
Volusia County FL (all 12 cities), Chicago IL (106 folders, 639 files),
Chipley FL, St Augustine FL, Bedford TX. ✓

/law
Chronicle + CourtListener federal opinions (SCOTUS + circuits).
Topic-based research with real citations from CourtListener search endpoint.
Federal court filter. Anti-hallucination prompt (no fabricated holdings).
/docket chain ready — every case links to full docket.
Working: qualified immunity (99,057 results, 8 displayed). ✓

/oral
CourtListener docket search + audio lookup (two-step pipeline).
SCOTUS + circuit court filter. Smart search adds "Supreme Court" context.
Chronicle index search. Oyez.org fallback for cases not in CourtListener.
Duration parsing (seconds → readable). Shared memory via _memory.py.
Working: Citizens United (real audio found), Dobbs, Roe v Wade, Trump v United States. ✓

Shared Memory (_memory.py)
Cross-command learning via UnifiedMemory + MemoryGuard.
Commands write results on success, recall prior searches on start.
Confidence threshold: 0.75. Source types: web_verified, chronicle.
Wired into: /oral. Ready for: /law, /judge, /docket, /jurisdiction. ✓

Stub Status
/state — not started. Mirror /federal but for state courts via jurisdiction files.

/statute — not started. Target: law.cornell.edu via webclaw_fetch.

/precedent — true stub (460 bytes). Replace entirely. Suggested: doctrine tracker by circuit.

/summarize — true stub (397 bytes). Replace entirely. Suggested: universal legal input → structured summary.

Patterns That Work
python
# LLM via A2A (every command uses this)
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
GET {COURTLISTENER_API}/audio/?docket=ID

# Shared memory
from agents.lawclaw.commands._memory import recall, remember, show_prior
Forbidden (DO NOT DO)
import anthropic or any direct LLM provider import

requests.get() in lawclaw commands (use webclaw_fetch via A2A)

Hardcoded lookup dicts when data exists in Chronicle

Silent exception handling (log everything)

DeepSeek will suggest requests.get() fallbacks when webclaw fails. Reject this. Unconstitutional.

Known Issues
URL noise in /federal results — some URLs from unrelated Chronicle hits leak in

SDNY judges page is JS-rendered — not fixable without headless browser in webclaw

CourtListener rate limits (429) on rapid successive queries — reduce page_size

/oral CourtListener audio database is sparse — Oyez fallback handles this honestly

Key Files
a2a_server.py — port 8766

agents/lawclaw/commands/ — all lawclaw commands

agents/lawclaw/commands/__init__.py — dynamic command loader

agents/lawclaw/commands/_memory.py — shared memory helper

agents/webclaw/core/chronicle_ledger.py — Chronicle interface

agents/webclaw/references/lawclaw/jurisdictions/us/ — all jurisdiction data

shared/llm/client.py — Sovereign Gateway

shared/memory/unified_memory.py — UnifiedMemory

shared/memory_guard.py — MemoryGuard (0.75 threshold)

.env — API tokens (COURTLISTENER_TOKEN, ANTHROPIC_API_KEY)

Session Log
2026-05-27: /docket complete. /federal working with Chronicle-first architecture.
/judge complete (FJC primary). /jurisdiction complete (3,800+ cities, GPS coordinates).
/law complete (SCOTUS + circuit opinions, real citations).
/oral complete (CourtListener + Chronicle + Oyez, memory wired).
_memory.py created for cross-command learning.
8 commands working. 4 stubs remain.