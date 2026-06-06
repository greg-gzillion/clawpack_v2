# CLAWPACK V2 — Chronicle Index Guide

## What is the Chronicle?

The Chronicle is the shared knowledge database for all 21 agents. It's a SQLite
database with FTS5 full-text search, located at `runtime/chronicle.db` (448MB, 35,000+ interactions).

## How Data Gets Into the Chronicle

### 1. Reference File Indexing
```bash
python scripts/index_all_references.py
```
Scans ALL markdown files in agents/webclaw/references/ and indexes full file
content, file paths as URLs, metadata, and coordinates.

### 2. WebClaw BM25 Pipeline
Every WebClaw search goes through: provider.search_structured() ->
chronicle.recover_by_context() -> merge + URL dedup -> BM25 ranking ->
source confidence weighting. Results are automatically indexed.

### 3. Agent cached_search()
When agents call cached_search(), results are cached to DataClaw:
- Location: agents/dataclaw/cache/{agent}/{query_hash}.json
- 24-hour TTL with automatic hit counting
- Cache miss -> WebClaw BM25 -> cache write
- Cache hit -> returns [CACHED] results instantly

### 4. Automatic Recording
Every time WebClaw fetches a URL, the content is recorded via
chronicle.record_fetch() with SHA-256 deduplication.

## How Agents Search the Chronicle

### Direct FTS5 Search
```python
results = agent.search_chronicle("Denver CO hospital", limit=10)
```

### Cache-First Retrieval (Recommended)
```python
result = agent.cached_search("ns:lawclaw Denver CO hospital")
```
Provides: DataClaw cache check -> WebClaw BM25 fallback -> auto-cache write.
Preserves BM25 score:, source:, and deduped from markers.

### Civic Data Lookups
Civic commands use Chronicle FTS5 directly via WebClaw's pipeline.
3,800+ city jurisdiction files organized by state/county/city.
Lookups return in 0.03-0.28s with zero LLM calls.

### FTS5 Full-Text Search
The Chronicle uses SQLite FTS5 for fast text search:
- Supports boolean operators: word1 OR word2
- Automatic keyword extraction on natural language queries
- Searches across county boundaries (city data is under county directories)
- `recover_by_context(query, limit)` — the canonical search method
- Three-tier fallback: FTS5 -> keyword extraction -> LIKE search

## Key Files

| File | Purpose |
|------|---------|
| runtime/chronicle.db | The SQLite database (448MB) |
| agents/webclaw/core/chronicle_ledger.py | ChronicleLedger class — record_fetch, recover_by_context |
| agents/webclaw/core/retriever.py | BM25 ranking + source confidence (global ranking governor) |
| shared/base_agent.py | search_chronicle(), cached_search() |
| shared/search_cache.py | DataClaw search cache (24hr TTL) |
| scripts/index_all_references.py | Rebuilds the index |

## Data Flow

```
webclaw/references/*.md
        ↓
index_all_references.py
        ↓
chronicle.db (FTS5 indexed)
        ↓
WebClaw BM25 pipeline (provider + chronicle + merge + dedup + source_weight)
        ↓
agent.cached_search()
        ↓
DataClaw cache (24hr TTL)
        ↓
Any of 21 agents
        ↓
LLM synthesis with citations (via Sovereign Gateway)
```

## What's Indexed

- **lawclaw**: 3,800+ city jurisdictions (courts, police, jails, hospitals, libraries, building permits)
- **mediclaw**: 91 medical specialties
- **txclaw**: 529 local files + 135 live docs.tx.org URLs across 17 domains
- **claw_coder**: 39 programming language references, 80+ technology categories
- **designclaw, drawclaw, docuclaw, draftclaw**: Design resources
- **All other agents**: Language, math, blockchain references

## Truncation Fixes (June 5, 2026)

Three truncation layers were preventing jurisdiction data from reaching agents:
| Layer | Was | Now |
|-------|-----|-----|
| search_cache.py | results[:5000] | results (full) |
| base_agent.py | cached['results'][:3000] | cached['results'] (full) |
| webclaw handler | ctx[:300] | ctx[:10000] |

These fixes enable complete jurisdiction file content (including ## Hospitals
sections at the end of files) to reach agent parsers.

## Known Limitations
- The index is organized by county, not city. FTS5 handles cross-boundary search.
- Only lawclaw actively populating DataClaw cache (June 5). Target: all retrieval agents.
- BM25 indexing is runtime-computed per request, not persistent (correct for current scale).
