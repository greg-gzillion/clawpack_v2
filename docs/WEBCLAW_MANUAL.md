# WEBCLAW ? COMPREHENSIVE MANUAL

## WHAT WEBCLAW IS

WebClaw is the online citation manager and intelligence layer for all 21 Clawpack agents. It does NOT just return search results. It fetches live URLs, extracts content, generates structured citations, and returns analyzed intelligence that agents feed to their LLMs.

## THREE RETRIEVAL LAYERS

### Layer 1: Live Web Fetching (webclaw.py)
- fetch_with_citation(url) ? fetches live URLs via requests + BeautifulSoup
- Extracts title, main content, cleans HTML (removes script/style/nav/footer/header)
- Returns structured citation: source domain, title, retrieval date
- Caches results in agents/webclaw/cache/

### Layer 2: SQLite Search Index (webclaw_provider.py)
- 280MB SQLite database at agents/webclaw/cache/web_cache.db
- 1.5M search terms across 20K indexed files
- search_with_context(query) ? returns content snippets with URLs
- Searches ALL agent namespaces ? no scoping (CONTAMINATION SOURCE)

### Layer 3: BM25 Retrieval with Source Confidence (retriever.py)
- BM25-ranked retrieval with configurable k1 and b parameters
- Integrates source_registry.py for domain trust scoring
- .gov domains score 0.92, state courts score 0.85
- Ranks by relevance, source quality, and freshness

## HOW AGENTS USE WEBCLAW

Every agent calls WebClaw through _gather_context():

`python
def _gather_context(self, query=""):
    parts = []
    web = self.call_agent("webclaw", f"search {query}", timeout=15)
    if web: parts.append("[WebClaw]: " + str(web)[:2000])  # RAW RESULTS
    chronicle_results = self.search_chronicle(query, limit=5)
    if chronicle_results:
        for c in chronicle_results:
            parts.append(c.get("context", "")[:1000])  # RAW CHRONICLE
    return "\n".join(parts)  # DUMPED DIRECTLY INTO LLM PROMPT
`

## THE CONTAMINATION PROBLEM

WebClaw searches ALL agent namespaces. When docuclaw searches for "business letter", WebClaw returns matches from lawclaw references, txclaw documentation, and any other namespace. The raw results (up to 2000 chars) are dumped directly into the LLM prompt. The LLM treats everything as source material.

This is why:
- /create business letter generates a nonprofit merger letter with IRS Form 990 references
- /create wedding invitation includes Sologenic API documentation
- /create job offer letter includes Morgan request-ID logging documentation

The fix requires:
1. Namespace-scoped search in webclaw_provider.py
2. Result summarization in _gather_context() instead of raw dump
3. Context length limits (currently 2000+ chars unrestricted)

## KEY FILES

| File | Purpose |
|------|---------|
| agents/webclaw/webclaw.py | Core class ? fetch_with_citation() |
| agents/webclaw/agent_handler.py | A2A handler ? routes search/fetch |
| agents/webclaw/providers/webclaw_provider.py | SQLite search ? search_with_context() |
| agents/webclaw/core/retriever.py | BM25 retrieval with source confidence |
| agents/webclaw/core/chronicle_ledger.py | Chronicle FTS5 ? recover_by_context() |
| agents/webclaw/references/ | 35,000+ reference files by agent namespace |
| agents/webclaw/cache/web_cache.db | 280MB SQLite, 1.5M terms, 20K files |
| runtime/chronicle.db | 448MB SQLite FTS5 index |

## THE REFERENCE CORPUS

Located at agents/webclaw/references/ ? 35,000+ files across 19 agent namespaces.
The jurisdiction dataset alone contains 50 states, 3,000+ counties, 3,800+ cities.
Each agent has its own subdirectory. Searches should be scoped to the calling agent.

## AGENT HANDLER FLOW

1. Agent sends: self.call_agent("webclaw", "search query", timeout=15)
2. Handler parses: fetch vs search vs raw URL
3. Search: provider.search_with_context(query) ? SQLite index
4. Chronicle: chronicle.recover_by_context(query, limit=2000000) ? FTS5
5. For Chronicle URLs: webclaw.fetch_with_citation(url) ? live fetch
6. Combined results returned to calling agent as raw string