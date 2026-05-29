# LawClaw — Law Research & Analysis Agent

21-agent ecosystem member. A2A on port 8766. Constitutional governance.

## What LawClaw Does
Legal research, case law lookup, docket retrieval, jurisdiction intelligence,
statute parsing, judge biographies, oral argument search, civic data lookup
across 3,800+ US cities, legal document generation, and legal translation
with term preservation.

## 25 Commands (all memory-wired, constitutional boundary enforced)

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

### Document Generation and Translation
- /doc [specs] — Generate jurisdiction-compliant legal documents via docuclaw with court data enrichment. Supports structured args: - plaintiff: [name] - defendant: [name] - case: [number] - grounds: [reason]
- /draft [specs] — Alias for /doc
- /translate [text|contract] — Legal translation with term preservation (Latin, French, citations, party names, court names). Chain: lawclaw -> interpretclaw -> docuclaw for formatted bilingual output
- /correct [fact|URL] — Community correction of facts/URLs via consensus engine with anti-pattern learning

### Navigation and Utility
- /list [state] [county] — Jurisdiction database navigator
- /browse [location] — Display jurisdiction files, auto-open URLs
- /search [query] — Local reference file search
- /analyze [text] — Comprehensive legal text analysis
- /ask [question] — AI law Q&A with Chronicle + WebClaw
- /brief [case name] — Case brief writer
- /stats — System statistics

## Architecture

### Constitutional Handler Boundary (23 systems)
Every command automatically passes through 23 constitutional checks:
Budget enforcement, Rate limiting, Circuit breaker, Metrics, Security audit,
Memory write, Learning extraction, Audit ledger, Consensus scoring,
Auditor logging, Health check, Telemetry, Lifecycle cleanup,
Enforcement gates, Guarded executor, Execution policy, Chronicle helper,
Procedural memory, Three-tier memory, Smart routing, Agent routing,
Schema validation, Structured logging, Shutdown registration, Hook management.

### Shared Memory
All commands use _memory.py for cross-command learning via UnifiedMemory + MemoryGuard.
Confidence threshold: 0.75. Source types: web_verified, chronicle.
Proven: /law "qualified immunity" surfaces prior searches across sessions.

### Shared Utilities
All commands use _helpers.py for LLM (Sovereign Gateway), Chronicle search, WebClaw fetch, CourtListener API.

### Cross-Agent Delegation
- /doc -> docuclaw with jurisdiction context + live court rules
- /translate -> interpretclaw (translate) -> docuclaw (format) for bilingual documents
- /plot, /code, /chart, /math -> capability registry routes to correct agent
- remember_court() / recall_court() handoff between /jurisdiction and /doc

### Capability Routing
Unrecognized commands are routed to the constitutional owner via shared/capabilities.py.
User types /plot bar sales in lawclaw -> silently routes to plotclaw. Article II preserved.

### Self-Improvement
- Consensus truth engine with structured claim extraction
- /correct command with anti-pattern learning via procedural memory
- Source registry: .gov at 0.92 authoritative, .us courts at 0.85 verified
- Truth resolver: .gov wildcard returns web_verified classification
- Memory staleness: facts carry age warnings

### Data Pipeline
- Court rules extractor reads 3,800-city jurisdiction files
- Location extraction handles structured args
- Filing-ready motions with correct state rules (FL 1.140(b)(6), NV 12(b)(6))
- Legal translation preserves Latin, French, citations, party names, court names
- All generated documents export to exports/ folder

## Key Files
- agent_handler.py — 23-system constitutional handler boundary, capability routing, /doc + /translate routes
- commands/_helpers.py — shared utilities (LLM, Chronicle, WebClaw, CourtListener, delegation)
- commands/_memory.py — shared memory bridge (remember_court, recall_court, show_prior)
- commands/*.py — 25 command implementations
- core/court_rules_extractor.py — multi-source extraction from jurisdiction files + live websites

## Data Sources
- CourtListener API (COURTLISTENER_TOKEN in .env)
- Chronicle index (448MB SQLite FTS5, shared with all 21 agents)
- Jurisdiction files (3,800+ cities in webclaw/references/lawclaw/jurisdictions/us/)
- FJC.gov (federal judge biographies)
- law.cornell.edu (statutes, rules)
- Oyez.org (oral arguments)

## Constitution Compliance
- All LLM access via A2A -> llmclaw -> Sovereign Gateway (Article I)
- All exceptions logged via log_err() — no except: pass (Article VII)
- Truth hierarchy: web_verified > chronicle > memory > inference (Article V)
- Cross-agent calls via call_agent() and capability registry (Article III)
- Handler boundary enforces all constitutional checks automatically
- LawClaw is the constitutional reference implementation for all 21 agents
- 100% shared infrastructure utilization (38/38 files connected)
