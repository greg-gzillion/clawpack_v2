# CLAWPACK V2 — Chronicle Index Guide

## What is the Chronicle?

The Chronicle is the shared knowledge database for all 21 agents. It's a SQLite database with FTS5 full-text search, located at `data/chronicle.db` (448MB, 35,000+ interactions).

## How Data Gets Into the Chronicle

### 1. Reference File Indexing
```bash
python scripts/index_all_references.py
Scans ALL markdown files in agents/webclaw/references/ and indexes full file content, file paths as URLs, metadata, and coordinates.

2. Automatic Recording
Every time WebClaw fetches a URL, the content is recorded via chronicle.record_fetch().

3. Agent Learning
When agents call _memory.remember(), facts are stored in unified memory and indexed.

4. Search Cache (DataClaw)
Web searches are cached for 24 hours in agents/dataclaw/cache/{agent_name}/. Repeat queries return cached results without hitting the web or using tokens.

How Agents Search the Chronicle
Direct Search (from any agent)
python
results = agent.search_chronicle("Denver CO hospital", limit=10)
Jurisdiction Lookup (from any agent)
python
hospitals = agent.lookup_jurisdiction("Denver CO", "hospital")
libraries = agent.lookup_jurisdiction("Miami FL", "library")
codes = agent.lookup_jurisdiction("Chicago IL", "building_codes")
Uses Chronicle FTS5 to search across 3,800+ city jurisdiction files organized by county.

Cached Web Search (from any agent)
python
results = agent.cached_search("qualified immunity", timeout=15)
First call hits webclaw and caches. Subsequent calls within 24hr return cached results.

FTS5 Full-Text Search
The Chronicle uses SQLite FTS5 for fast text search:

Supports boolean operators: word1 OR word2

Automatic keyword extraction on natural language queries

Searches across county boundaries (city data is under county directories)

recover_by_context(query, limit) — the canonical search method

Key Files
FilePurpose
data/chronicle.dbThe SQLite database (448MB)
agents/webclaw/core/chronicle_ledger.pyChronicleLedger class — record_fetch, recover_by_context
shared/base_agent.pysearch_chronicle(), lookup_jurisdiction(), cached_search()
shared/search_cache.pyDataClaw search cache (24hr TTL)
scripts/index_all_references.pyRebuilds the index
scripts/check_index.pyShows index statistics
Data Flow
text
webclaw/references/*.md
        ↓
index_all_references.py
        ↓
chronicle.db (FTS5 indexed)
        ↓
BaseAgent.search_chronicle() / lookup_jurisdiction()
        ↓
Any of 21 agents
        ↓
LLM synthesis with citations (via Sovereign Gateway)
        ↓
Results cached to DataClaw (24hr TTL)
What's Indexed
lawclaw: 3,800+ city jurisdictions (courts, police, jails, hospitals, libraries, building permits)

mediclaw: 91 medical specialties

txclaw: 60+ blockchain documentation categories

claw_coder: 39 programming language references

designclaw, drawclaw, docuclaw, draftclaw: Design resources

All other agents: Language, math, blockchain references

Known Limitations
- The index is organized by county, not city. FTS5 handles cross-boundary search.
- recover_by_context() has 19 call sites with minor signature drift. Non-blocking warnings.
- ChronicleLedger exports: ChronicleLedger, get_chronicle, record_fetch, recover_by_context.
  Do not import log_event or call get_timeline. Neither exists (resolved May 30, 2026).
- Civic commands use Chronicle FTS5 directly via lookup_jurisdiction(). 0.03-0.28s. No LLM calls.

log_event is not a top-level export — use chronicle.record_fetch() instead

The index is organized by county, not city — FTS5 handles cross-boundary search
