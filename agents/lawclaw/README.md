# LawClaw — Law Research & Analysis Agent

21-agent ecosystem member. A2A on port 8766. Constitutional governance.

## What LawClaw Does
Legal research, case law lookup, docket retrieval, jurisdiction intelligence,
statute parsing, judge biographies, oral argument search, and civic data lookup
across 3,800+ US cities.

## 23 Commands (all memory-wired)

### Core Legal Research
- /law [topic] — Chronicle + CourtListener (SCOTUS + circuits), exact phrase search, authority ranking
- /docket [case number|URL] — CourtListener API, paginated entries, jury demand, LLM summaries
- /cite [citation] — Citation parsing with concept router, Chronicle + WebClaw + LLM
- /precedent [doctrine] — Doctrine tracker by circuit, SCOTUS + circuits, cross-agent offers
- /oral [case name] — CourtListener audio lookup, Chronicle + Oyez fallback
- /summarize [input] — Universal legal input summarizer
- /statute [citation] — law.cornell.edu fetching, USC/UCC/FRCP/FRE/FRAP/state

### Court Systems
- /federal [query] — Chronicle-first, circuits/SCOTUS/PACER/FRCP/city lookups
- /state [state] [county] — State court lookup, county list + court details
- /court [location] — Filesystem jurisdiction lookup, .gov URL ranking

### Judicial and Civic Intelligence
- /judge [name] — FJC biography + CourtListener positions + Chronicle
- /jurisdiction [city] [state] — 3,800+ cities, courts/police/jail/hospitals/libraries
- /police [city] [state] — Police department lookup
- /detention [city] [state] — Jail/detention facility lookup
- /library [city] [state] — Library lookup with legal resource discovery
- /hospital [city] [state] — Hospital lookup with GPS coordinates

### Navigation and Utility
- /list [state] [county] — Jurisdiction database navigator
- /browse [location] — Display jurisdiction files, auto-open URLs
- /search [query] — Local reference file search
- /analyze [text] — Comprehensive legal text analysis
- /ask [question] — AI law Q&A with Chronicle + WebClaw
- /brief [case name] — Case brief writer
- /stats — System statistics

## Architecture

### Shared Memory
All commands use _memory.py for cross-command learning.
Confidence threshold: 0.75. Source types: web_verified, chronicle.

### Shared Utilities
All commands use _helpers.py for LLM, Chronicle, WebClaw, CourtListener.

### Cross-Agent Delegation
delegate("docuclaw", "/create {content}") creates documents.
delegate("plotclaw", "/plot {data}") creates charts.

## Key Files
- agent_handler.py — A2A handler, command routing
- commands/_helpers.py — shared utilities
- commands/_memory.py — shared memory bridge
- commands/*.py — 23 command implementations

## Data Sources
- CourtListener API (COURTLISTENER_TOKEN in .env)
- Chronicle index (448MB SQLite, shared with all 21 agents)
- Jurisdiction files (3,800+ cities)
- FJC.gov, law.cornell.edu, Oyez.org

## Constitution Compliance
- All LLM access via A2A to llmclaw to Sovereign Gateway
- All exceptions logged (no except: pass)
- Truth hierarchy: web_verified > chronicle > memory > inference
- Cross-agent calls via call_agent() or delegate()
