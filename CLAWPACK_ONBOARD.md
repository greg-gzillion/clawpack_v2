> READ THIS FIRST. Do not write any code until you have read this entire document.

# CLAWPACK V2 — AI ONBOARDING CONTEXT

## What This Is
21-agent AI ecosystem. Menu-driven CLI. A2A routing on port 8766.
448MB Chronicle SQLite index at data/chronicle.db. Constitutional governance.
Built by Greg. You are helping build lawclaw commands.

## Before You Write Any Code
1. Ask to see the current file if modifying an existing command.
2. Ask to see a working command (e.g. docket.py) if building a new stub.
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
    _log("lawclaw", "command_timeout", url)
except Exception as e:
    _log("lawclaw", "command_error", str(e)[:200])
Working Commands
/docket — CourtListener API, real docket entries, jury demand, LLM summaries ✓

/court — Filesystem jurisdiction lookup, URL ranking ✓

/cite — Citation parsing with concept router ✓

/federal — Chronicle-first, filesystem-backed. NO HARDCODED DICTS.
Uses chronicle_search(), search_jurisdiction_files(), cl_get(), webclaw_fetch().
Working: circuits, supreme, pacer, frcp, Bedford VA city lookups.
SDNY judges: page is JS-rendered. WebClaw returns metadata only. Honest fallback in place — NOT a bug, don't "fix" it.

/judge — FJC biography + CourtListener positions + Chronicle. Working: Sotomayor, Pitman.
CourtListener /people/ is sparse — FJC is primary source. ✓

/jurisdiction — Chronicle + filesystem civic intelligence. City and county lookup.
Courts, police, jail, hospitals with GPS, library, permits. 3,800+ cities indexed.
Working: Bedford VA, Daytona Beach FL, Volusia County FL, Chicago IL, Chipley FL,
St Augustine FL, Bedford TX. ✓

/law — Chronicle + CourtListener federal opinions (SCOTUS + circuits).
Topic-based research, real citations, /docket chain ready.
Working: qualified immunity ✓
Note: Do not summarize case holdings without full text in data.

Stub Status
/state — not started. Mirror /federal but for state courts via jurisdiction files.

/statute — not started. Target: law.cornell.edu via webclaw_fetch.

/oral, /precedent, /summarize — true stubs (197-460 bytes), replace entirely.

Patterns That Work
python
# LLM via A2A
resp = requests.post(f"{A2A}/v1/message/llmclaw",
    json={"task": f"/llm {prompt}", "agent": "lawclaw"}, timeout=120)

# WebClaw fetch
resp = requests.post(f"{A2A}/v1/message/webclaw",
    json={"task": f"fetch {url}", "agent": "lawclaw"}, timeout=20)

# Chronicle search
from agents.webclaw.core.chronicle_ledger import get_chronicle
c = get_chronicle()
results = c.recover_by_context("query", limit=10)

# Filesystem jurisdiction search
LAW_REFS = Path(__file__).parent.parent.parent.parent / "agents" / "webclaw" / "references" / "lawclaw"
for md_file in (LAW_REFS / "jurisdictions" / "us").rglob("*.md"):
    content = md_file.read_text(encoding='utf-8', errors='ignore')

# CourtListener API
token from .env (COURTLISTENER_TOKEN)
GET {COURTLISTENER_API}/opinions/?court=scotus
GET {COURTLISTENER_API}/dockets/?docket_number=X
Forbidden (DO NOT DO)
import anthropic or any direct LLM provider import

requests.get() in lawclaw commands (use webclaw_fetch via A2A)

Hardcoded lookup dicts when data exists in Chronicle or CIRCUITS

Silent exception handling (log everything)

DeepSeek will suggest requests.get() fallbacks when webclaw fails. Reject this. It is unconstitutional.

Known Issues
URL noise in /federal results — some URLs from unrelated Chronicle hits leak in (pending fix)

SDNY judges page is JS-rendered — not fixable without headless browser in webclaw

Key Files
a2a_server.py — port 8766

agents/lawclaw/commands/ — all lawclaw commands

agents/lawclaw/commands/__init__.py — dynamic command loader

agents/webclaw/core/chronicle_ledger.py — Chronicle interface

agents/webclaw/references/lawclaw/jurisdictions/us/ — all jurisdiction data

shared/llm/client.py — Sovereign Gateway

.env — API tokens

Session Log
2026-05-27: /docket complete. /federal working. SDNY judges JS-limitation documented.
/judge complete (FJC primary, CourtListener supplemental).
/jurisdiction complete (3,800+ cities, hospitals with GPS, civic intelligence).
/law complete (SCOTUS + circuit opinions, topic research with real citations).
CLAWPACK_ONBOARD.md created. 4 commands built today. 3 stubs remain.