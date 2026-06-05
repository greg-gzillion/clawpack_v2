# WEBCLAW — COMPREHENSIVE MANUAL

## WHAT WEBCLAW IS

WebClaw is the central nervous system of Clawpack V2. It is NOT a search engine.
It is the unified retrieval and knowledge layer for all 21 agents. Every agent
depends on it. No agent works without it.

WebClaw fetches live URLs, queries the Chronicle FTS5 memory index, searches the
35,000+ file reference corpus, merges results, deduplicates by URL, ranks via BM25
with source confidence scoring, and returns structured intelligence that agents feed
to their LLMs through the Sovereign Gateway.

## THREE RETRIEVAL LAYERS

### Layer 1: Live Web Fetching (webclaw.py)
- `fetch_with_citation(url)` — fetches live URLs via requests + BeautifulSoup
- Extracts title, main content, cleans HTML (removes script/style/nav/footer/header)
- Returns structured citation: source domain, title, retrieval date
- Caches results in `agents/webclaw/cache/`

### Layer 2: SQLite Search Index (webclaw_provider.py)
- 280MB SQLite database at `agents/webclaw/cache/web_cache.db`
- 1.5M search terms across 20K indexed files
- `search_with_context(query, namespace)` — returns content snippets, namespace-scoped
- `search_structured(query, namespace)` — returns List[Dict] for BM25 ranking
- Namespace scoping via `ns:` prefix prevents cross-domain contamination

### Layer 3: Chronicle FTS5 Memory Index (chronicle_ledger.py)
- 448MB SQLite FTS5 database at `runtime/chronicle.db`
- 35,000+ indexed reference files and agent interactions
- `recover_by_context(query, limit)` — full-text search with keyword fallback
- `record_fetch(url, context, source)` — immutable audit trail with SHA-256 dedup
- Civic lookups: 0.03-0.28s via direct FTS5 (zero LLM calls)

## RANKING LAYER: BM25 + Source Confidence (retriever.py)

BM25 is the final ranking authority over the merged candidate set from all three
retrieval layers. The ranking formula is:

```
final_score = bm25_score * source_weight
```

- `bm25_score` — BM25 relevance with configurable k1=1.5, b=0.75
- `source_weight` — domain trust from `shared/source_registry.py`
- .gov domains score 0.92, state courts score 0.85
- **source_registry is a global ranking governor**: changing trust values
  affects retrieval order for all 21 agents

## HOW AGENTS USE WEBCLAW

Agents call WebClaw through the A2A message bus:

```python
self.call_agent("webclaw", "search ns:lawclaw query", timeout=15)
```

The `ns:` prefix scopes the search to the calling agent's reference namespace.
Chronicle context is no longer injected into generic `ask_llm()` prompts (fixed
June 4, 2026).

## SEARCH REQUEST FLOW

```
1. Agent sends: call_agent("webclaw", "search ns:lawclaw court Denver")
2. Handler extracts namespace (ns:lawclaw) and query (court Denver)
3. provider.search_structured(query, namespace="lawclaw") -> 20 candidates
4. chronicle.recover_by_context(query, limit=10) -> 10 memory candidates
5. Merge candidates -> deduplicate by URL
6. BM25.index(deduped) -> BM25.search(query, top_k=10)
7. final_score = bm25_score * source_weight
8. Return ranked results with [score: X.XXX, source: X.XX]
```

## THE CONTAMINATION PROBLEM (RESOLVED)

Before June 4, 2026, WebClaw searched ALL agent namespaces regardless of which
agent was asking. A docuclaw search for "business letter" would return lawclaw
legal references, txclaw blockchain docs, and claw_coder Next.js config files.

The fix (now active):
1. Namespace-scoped search via `ns:{agent}` prefix on all 19 agents
2. Chronicle context removed from BaseAgent.ask_llm()
3. Gateway prompt caps (4000 chars for local models)
4. BM25 + source confidence provides relevance filtering

## THE REFERENCE CORPUS

Located at `agents/webclaw/references/` — 35,000+ files across 19 agent namespaces.
The jurisdiction dataset alone contains 50 states, 3,000+ counties, 3,800+ cities,
13 tribal nations, and 5 US territories with municipal court data, police, jails,
hospitals (with GPS coordinates), libraries, and building permit offices.

Each agent has its own reference subdirectory: lawclaw, mediclaw, txclaw,
draftclaw, designclaw, claw_coder, and 13 more.

## KEY FILES

| File | Purpose |
|------|---------|
| `agents/webclaw/webclaw.py` | Live web fetch with citations |
| `agents/webclaw/agent_handler.py` | A2A handler, search/fetch routing, BM25 orchestration |
| `agents/webclaw/providers/webclaw_provider.py` | SQLite search, namespace scoping, structured output |
| `agents/webclaw/core/retriever.py` | BM25 ranking with source confidence (global ranking governor) |
| `agents/webclaw/core/chronicle_ledger.py` | Chronicle FTS5, record_fetch, recover_by_context |
| `agents/webclaw/core/cache.py` | URL cache with TTL, hit counting |
| `agents/webclaw/core/rate_limiter.py` | Domain rate limiting + robots.txt compliance |
| `agents/webclaw/references/` | 35,000+ reference files organized by agent namespace |
| `agents/webclaw/cache/web_cache.db` | 280MB SQLite, 1.5M terms, 20K files |
| `runtime/chronicle.db` | 448MB SQLite FTS5 index |

## ARCHITECTURE VERSION

- Version: 3.2.0 (June 5, 2026)
- BM25 wired into production query path
- Provider + Chronicle merge with URL deduplication
- Source confidence scoring active on all queries
- Namespace scoping active on all 19 agents
- All V1 artifacts removed (config.py, shared_memory.py, api.py)
