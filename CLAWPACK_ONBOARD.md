# CLAWPACK V2 — AI ONBOARDING CONTEXT

## What This Is
21-agent AI ecosystem. Menu-driven CLI. A2A routing on port 8766.
448MB Chronicle SQLite index at runtime/chronicle.db. Constitutional governance.
Built by Greg.

## RUN THIS FIRST
`python scripts/onboard.py` — prints everything you need to understand this system.
It prints all required documents in order. Run it. Read the output.
CRITICAL: Read docs/KNOWN_TRAPS.md before writing any code.
Also read: docs/READ_THIS_FIRST.md for quick start.
Also read: docs/WEBCLAW_MANUAL.md for the complete WebClaw guide.

## CRITICAL: PowerShell Environment (Windows)
- NEVER use python -c with multi-line code. Write to scripts/_temp.py and run it.
- NEVER pipe to Out-File for files over 100 lines. PowerShell silently truncates.
- NEVER use PowerShell heredocs with Python code. They eat escape characters.
- ECHO WORKS for small files. Copy-Item WORKS for deployment.
- Pattern B WORKS for large files: Python builds content as list of lines, joins, writes.
- ALWAYS verify writes immediately.
- ALWAYS kill Python: taskkill /F /IM python.exe
- ALWAYS clear __pycache__ after changing shared modules.
- READ POWERSHELL_SURVIVAL_GUIDE.md for full failure patterns and fixes.

## Before You Write Any Code
1. Ask to see the current file if modifying an existing command.
2. Ask to see a working command if building a new stub.
3. Do not assume file contents — they may differ from conversation history.
4. State what you are about to do before doing it. One function at a time.

## How Commands Load
Commands in each agent commands/ directory are loaded dynamically.
Each file needs: name = "/commandname" and def run(args, agent=None) at module level.
No manual registration — just drop the .py file in the directory.
This is the preferred pattern for adding features to all agents.
Do NOT batch-inject code into handlers. It corrupts indentation.
Write a command file once, then Copy-Item to all agents.

## CRITICAL LESSON: Command Files vs Handler Injection
On May 30, batch-injecting /voice code into 21 agent handlers via string replacement
corrupted indentation in ALL 21 agents. Required git revert to clean state.
The fix: write command files in agents/lawclaw/commands/, then Copy-Item to all others.
Zero handler changes. Zero indentation risk. The system was designed for this.

## Constitution (NON-NEGOTIABLE)
- All LLM access goes to Sovereign Gateway only (shared/llm/client.py). No direct API calls.
- All exceptions must log. except: pass is UNCONSTITUTIONAL.
- Truth hierarchy: web_verified > chronicle > memory > inference.
- Every agent has defined jurisdiction. No crossing.

---

## Current State — June 4, 2026 -- LLMCLaw CONSOLIDATION + WEBCLAW NAMESPACE SCOPING + PROVIDER CHAIN FIXES
llmclaw: 4 llm*.py variants consolidated to 1 llm.py. /use fixed.
Sovereign Gateway: direct_model first-class provider. Prompt cap 4000 chars for local models.
WebClaw: namespace-scoped SQL search. ns:{agent} on all 19 agents. Chronicle removed from ask_llm().
FlowClaw: 13 variants inventoried. RustPyCraw: Article I violation resolved.
Scripts: 161 deleted, 16 kept. Version bumped to 3.2.0.

June 3, 2026

### Runtime Health
| Metric | Value |
|--------|-------|
| Agent availability | 21/21 responsive |
| A2A transport | Healthy (port 8766) |
| Chronicle index | 35,000+ interactions (runtime/chronicle.db) |
| LLM providers | Ollama primary, Groq/OpenRouter fallback |
| Provider chain | Ollama(gemma3:4b) -> Groq -> OpenRouter -> Anthropic |
| Active model | gemma3:4b (3.3GB, fits GTX 970 GPU) |
| Lifecycle cleanup errors | 0 |
| Enforcement | Active — 6 sovereignty patterns blocked at HTTP boundary |
| Civic commands | Chronicle FTS5 direct (0.03-0.28s) |
| Memory filtering | Geographic scoring bonus active (city +5, state +3) |

---

## WEBCLAW — THE CENTRAL KNOWLEDGE SYSTEM

### What WebClaw Is
WebClaw is the intelligence layer for all 21 Clawpack agents. It is NOT a URL relay or
search result passthrough. It must analyze web content, extract meaning, and return
intelligent details that agents can use as factual context for LLM prompts.

Every agent calls WebClaw through `_gather_context()`. WebClaw searches across three
retrieval layers and returns combined results. The agent feeds those results to the LLM.
If WebClaw returns garbage, every agent produces garbage. If WebClaw returns raw URLs
instead of analyzed intelligence, agents hallucinate.

### Three Retrieval Layers

**Layer 1: Live Web Fetching (webclaw.py)**
- `fetch_with_citation(url)` — fetches real URLs via requests + BeautifulSoup
- Extracts title, main content, cleans HTML (removes script/style/nav/footer/header)
- Returns structured citation: source domain, title, retrieval date
- Caches results in agents/webclaw/cache/
- This is where intelligence extraction should happen — currently returns raw page text

**Layer 2: SQLite Search Index (webclaw_provider.py)**
- 280MB SQLite database at agents/webclaw/cache/web_cache.db
- 1.5M search terms across 20K indexed files
- `search_with_context(query)` — returns content snippets with URLs
- Searches ALL agent namespaces with no scoping — THIS IS THE CONTAMINATION SOURCE

**Layer 3: BM25 Retrieval with Source Confidence (retriever.py)**
- BM25-ranked retrieval with configurable k1 and b parameters
- Integrates source_registry.py for domain trust scoring
- .gov domains score 0.92, state courts score 0.85
- Ranks by relevance, source quality, and freshness

### The Reference Corpus
Located at `agents/webclaw/references/` — this is the canonical knowledge base for
the entire Clawpack ecosystem. 35,000+ files organized by agent namespace.
agents/webclaw/references/
├── claw_coder/ — 80+ technology categories (python, rust, react, docker, etc.)
│ ├── python/ — Python references
│ ├── rust/ — Rust references
│ ├── javascript/ — JavaScript references
│ ├── OPERATING_RULES.md
│ ├── REFERENCE_RANKING.md
│ ├── SYSTEM_OVERVIEW.md
│ └── ... (80+ technology directories)
├── lawclaw/ — 3,800+ city jurisdictions across 50 states
│ └── jurisdictions/us/{State}/{County}/{City}/
│ ├── municipal_court.md
│ ├── building_code.md
│ ├── law_resources.md
│ └── medi_resources.md
├── mediclaw/ — 91 medical specialties
├── txclaw/ — 60+ blockchain documentation categories
├── draftclaw/ — 4,744 building code entries
├── designclaw/ — Design resources, 50 states
├── docuclaw/ — Document templates
├── drawclaw/ — Art resources
├── dreamclaw/ — AI vision resources
├── crustyclaw/ — Rust references
├── dataclaw/ — Data processing references
├── fileclaw/ — File format references
├── flowclaw/ — Diagram references
├── interpretclaw/ — Translation references
├── langclaw/ — Language teaching references
├── liberateclaw/ — Model liberation references
├── mathematicaclaw/ — Math references
├── plotclaw/ — Chart references
├── rustypycraw/ — Code crawling references
└── MASTER_ATTRIBUTION_INDEX.md

text

### The Jurisdiction Dataset
Located at `references/lawclaw/jurisdictions/us/`:
- 50 states + DC
- 3,000+ counties/parishes/boroughs
- 3,800+ cities/towns
- 13 tribal nations with court data
- 5 US territories
- Federal court system
- 4,744 building code entries
- 15,000+ court entries

Organization: `{State}/{County}/{City}/`

Example — West Virginia (55 counties, 100+ cities):
us/WV/
├── Kanawha/Charleston_WV/ — Municipal court, building codes
├── Monongalia/Morgantown/
├── Berkeley/Martinsburg/
├── state/ — State-level design/docu/draw/medi resources
└── ...

text

This dataset was populated over weeks by fetching real government websites, court
systems, and municipal data sources. Each city folder contains municipal court data,
police department info, jail/detention facilities, hospital locations with GPS
coordinates, library locations, and building permit offices.

### How Agents Use WebClaw
Every agent's `_gather_context()` follows this pattern:

```python
def _gather_context(self, query=""):
    parts = []
    web = self.call_agent("webclaw", f"search {query}", timeout=15)
    if web: parts.append("[WebClaw]: " + str(web)[:2000])  # RAW RESULTS
    chronicle_results = self.search_chronicle(query, limit=5)
    if chronicle_results:
        for c in chronicle_results:
            parts.append(c.get("context", "")[:1000])  # RAW CHRONICLE
    return "\n".join(parts)  # DUMPED DIRECTLY INTO LLM PROMPT
The raw results (up to 2000 chars) are dumped directly into the LLM prompt with no
filtering, no summarization, and no namespace scoping.

The Contamination Problem (CRITICAL BUG)
WebClaw searches ALL agent namespaces regardless of which agent is asking. When
docuclaw searches for "business letter", WebClaw returns matches from lawclaw
references, txclaw documentation, Morgan docs, Sologenic API specs, and Next.js
config files — because all namespaces are searched.

This is why:

/create business letter generates a nonprofit merger letter with IRS Form 990 references

/create wedding invitation includes Organization Service REST API documentation

/create job offer letter includes Morgan request-ID logging documentation

/create project proposal includes Next.js allowedDevOrigins configuration

The fix requires:

Namespace-scoped search in webclaw_provider.py (search only the calling agent's references)

Result summarization in _gather_context() instead of raw content dump

Context length limits (currently 2000+ chars unrestricted)

WebClaw must return analyzed intelligence, not raw page content or URLs

Key WebClaw Files
File	Purpose
agents/webclaw/webclaw.py	Core class — fetch_with_citation(url)
agents/webclaw/agent_handler.py	A2A handler — routes search/fetch requests
agents/webclaw/providers/webclaw_provider.py	SQLite search — search_with_context()
agents/webclaw/core/retriever.py	BM25 retrieval with source confidence scoring
agents/webclaw/core/chronicle_ledger.py	Chronicle FTS5 — recover_by_context(), record_fetch()
agents/webclaw/core/cache.py	WebCache for fetched URLs
agents/webclaw/core/rate_limiter.py	RateLimiter + RobotsTxtParser
agents/webclaw/utils/content_parser.py	TextExtractor for HTML content
agents/webclaw/references/	35,000+ reference files organized by agent namespace
agents/webclaw/cache/web_cache.db	280MB SQLite, 1.5M terms, 20K files
runtime/chronicle.db	448MB SQLite FTS5 index
Agent Accessibility (all via command files, no handler changes)
Feature	Agents	How to use
/voice	21/21	Toggle system-wide voice mode
/listen	21/21	One-shot microphone transcription
/translate	21/21	Detect language and translate to English
/braille	21/21	Convert text to Braille Unicode output
/speak	21/21	Speak text aloud in current language
/read	21/21	TTS reader with voice profiles, file reading, speed control
/language	21/21	Set system-wide language preference
/interpret	21/21	Live bidirectional interpreter mode
/access	21/21	Toggle Braille/Neuralink/Eye tracking on/off
Provider Chain (Sovereign Gateway)
Priority	Provider	Model	Latency	Cost
1	Ollama	gemma3:4b	0.8s GPU	Free (local)
2	Groq	llama-3.3-70b-versatile	0.7s	Free (rate-limited)
3	OpenRouter	google/gemma-4-26b-a4b-it:free	0.7s	Free tier
4	Anthropic	claude-haiku-4-5-20251001	1.2s	Paid
GPU: NVIDIA GeForce GTX 970, 4GB VRAM (~2.8GB available).
Fits GPU: tinyllama (0.6GB), gemma3:1b (0.8GB), gemma3:4b (3.3GB), smollm2 (3.4GB).
Does NOT fit: deepseek-r1:8b (5.2GB), codellama:7b (3.8GB), gemma3:12b+.
Obliterated models (6): codellama_7b, deepseek_coder_6.7b, phi2, qwen_coder_7b, smollm2_1.7b, tinyllama.
Switch model: llmclaw> /use MODEL_NAME

System-Wide Accessibility Toggles
Toggle	Hotkey	Wake Word	Menu Key
Voice mode	Ctrl+Alt+V	start/stop listening	v
Braille output	Ctrl+Alt+B	—	b
Neuralink	Ctrl+Alt+N	—	n
Eye tracking	Ctrl+Alt+E	—	e
Quick Reference: Files That Matter
File	Purpose	Status
a2a_server.py	Central message bus, port 8766	Active
shared/llm/client.py	Sovereign Gateway	Active
shared/llm/providers/init.py	Provider detection + chain order	Active
shared/base_agent.py	Foundation class for all 21 agents	Active
shared/_agent_helpers.py	Empire-wide utility belt	Active
shared/enforcement/detector.py	ForbiddenPatternDetector (sovereignty)	Active
shared/enforcement/engine.py	Full EnforcementEngine	Dormant
shared/memory/unified_memory.py	Cross-agent shared memory	Active
shared/query_normalizer.py	Canonical location extraction + geo-filtering	Active
shared/accessibility.py	TTS/STT/Braille/Translate	Active
shared/lifecycle.py	Agent cleanup supervisor	Active (0 errors)
agents/lawclaw/agent_handler.py	Reference implementation	Gold standard
agents/webclaw/agent_handler.py	WebClaw A2A handler	Active
agents/webclaw/references/	35,000+ reference files by agent namespace	Active
agents/webclaw/core/chronicle_ledger.py	Chronicle FTS5 index	Active
agents/llmclaw/agent_handler.py	Model manager + orchestrator	Active
runtime/chronicle.db	448MB SQLite FTS5	Active
runtime/ledgers/	Constitutional ledger, budget, chronicle	Active
runtime/indexes/	Memory and consensus indexes	Active
data/	Static reference data only (jurisdictions, schemas)	Active
models/active_model.json	Active model + provider priorities	Active
scripts/onboard.py	Complete system onboarding — RUN THIS FIRST	Active
docs/WEBCLAW_MANUAL.md	Comprehensive WebClaw guide	Active
Session Log
June 4, 2026 -- LLMCLaw CONSOLIDATION + WEBCLAW NAMESPACE SCOPING + PROVIDER CHAIN FIXES
llmclaw: 4 llm*.py variants consolidated to 1 llm.py. /use fixed.
Sovereign Gateway: direct_model first-class provider. Prompt cap 4000 chars for local models.
WebClaw: namespace-scoped SQL search. ns:{agent} on all 19 agents. Chronicle removed from ask_llm().
FlowClaw: 13 variants inventoried. RustPyCraw: Article I violation resolved.
Scripts: 161 deleted, 16 kept. Version bumped to 3.2.0.

June 3, 2026 — DOCUCLAW + FLOWCLAW FIXES + DOCUMENTATION
DocuClaw handler: Fixed document generation pipeline. Removed template routing and
keyword detection. Clean research-via-webclaw -> LLM -> validate -> view -> export.
Added intent detection: drafting mode for simple requests, research mode for legal/
regulatory queries. Provider chain now respects active_model.json priority order.

FlowClaw handler: Rewritten. Removed dead 23-system boundary block. Fixed diagram
commands (/flowchart, /sequence, /architecture, /mindmap). Added inline browser
popup viewer with Mermaid.js rendering. All 6 commands verified working.

WebClaw documentation: Created docs/WEBCLAW_MANUAL.md (83 lines) documenting the
three-layer retrieval system. Created docs/WEBCLAW_ARCHITECTURE.md (165 lines).
Documented the contamination problem with real examples and fix requirements.

Onboard script: Complete rewrite. Single command gives next AI agent everything:
architecture, rules, WebClaw details, provider chain, known issues, next mission,
and prints all 9 required documents. Zero syntax errors, zero null bytes.

Docs cleanup: Deleted stale auto-generated files. Renamed historical docs with dates.
Created cat_onboard.py to print all required reading. Updated README with model
selection guide for beginners based on hardware capabilities.

June 2, 2026 — ENFORCEMENT + RUNTIME SEPARATION + GEO-FILTERING
Priority 1 — Enforcement blocking: DONE

6 sovereignty patterns return 403 at HTTP boundary.

except:pass anti-pattern removed. Architectural decision logged.

Priority 2 — Ledger repair: RESOLVED

36 entries, valid JSON, hash chain intact. Fixed by runtime migration.

Priority 3 — Geographic memory filtering: DONE

_extract_location() extracts city/state. +5 same-city, +3 same-state bonus.

8/8 test cases pass. Bedford VA contamination prevented.

Consolidated into shared/query_normalizer.py.

Priority 4 — Provider fallback validation: DONE

test_fallback_chain.py created. Groq + OpenRouter confirmed working.

Priority 5 — Agent validation: DONE

All 21 agents tested and responsive.

Runtime state separation: DONE

All mutable files moved from data/ to runtime/. runtime/ gitignored.

10 source files patched. 2 absolute path bugs fixed.

Obliterated models listing: FIXED

/models reads from models/obliterated/ directory with metadata.

claw_coder handler cleanup: DONE

75 lines of dead 23-system boundary block removed.

State audit published at docs/reports/STATE_OF_CLAWPACK_V2_2026_06_02.md
Scores: Enforcement 3.0->6.0, Infrastructure 8.5->9.0, Overall 6.6->7.0

May 31 / June 1, 2026
Court resolver: city-first traversal. Georgetown CO resolves in ~500ms.

Accessibility layer unified. Event bus created. Voice pipeline functional.

May 30, 2026
Handler injection failure: ALL 21 agents corrupted. Git revert required.

Command-file deployment adopted as the only safe extension mechanism.

Lifecycle contract drift resolved (3 errors -> 0).

Provider chain fixed. Accessibility commands deployed to all 21 agents.

May 27-29, 2026
12 lawclaw commands built. Cross-agent flow established.

Constitutional boundary activated. Consensus engine deployed.

NEXT SESSION MISSION
Priority 6: Codebase Consolidation (IN PROGRESS -- llmclaw DONE, flowclaw inventoried, scripts cleaned)
Agent	Variants	Action	Risk
flowclaw	13 flowclaw*.py files	Inventory first, then consolidate to 1	Medium
docuclaw	3 implementations	Keep agent_handler.py, archive others	Medium
mediclaw	3 Ollama providers, 2 OpenRouter	Deduplicate to 1 each	Low
llmclaw	4 llm*.py variants	Consolidate to 1	Low
webclaw	2 A2A servers	Keep one, remove a2a/integrated_server.py	Low
langclaw	langclaw_backup/	Delete	Low
FLOWCLAW RULE: No deletions in first session. READ-ONLY inventory.
Map which file agent_handler.py imports. Find unique functionality.
Build dependency map. Only then decide what moves to _archive/.

Quick Win: STATE_NAMES Deduplication
Four separate STATE_NAMES dicts. Import from shared/query_normalizer instead.
Files: list.py, state.py, jurisdiction_engine.py. 5 min, zero risk.

Priority 7: Security Assessment
Prompt injection, memory poisoning, privilege escalation.

Activate guarded_executor.py. Run ForbiddenPatternDetector against all handlers.

Infrastructure
WebClaw namespace-scoped search (CRITICAL — fixes contamination bug)

Beta Gate Progress (5 of 10 passed)
#	Requirement	Status
1	Enforcement blocks violations	DONE
2	Constitutional ledger repaired	DONE
3	Memory geographic filtering	DONE
4	All 21 agents tested	DONE
5	Provider fallback validated	DONE
6	Duplicate implementations reduced	IN PROGRESS
7	Coverage tests added	NOT STARTED
8	Installation tested clean Windows	NOT STARTED
9	Installation tested clean Linux	NOT STARTED
10	Security review completed	NOT STARTED