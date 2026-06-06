# AGENT_CAPABILITIES.md — Constitutional Capability Registry

## Capability-to-Agent Mapping

Every capability has exactly one constitutional owner. This prevents jurisdiction conflicts.

| Capability | Constitutional Owner | Key Commands | Notes |
|-----------|---------------------|----------|-------|
| **Legal Research** | lawclaw | /law, /docket, /cite, /precedent, /court, /judge, /jurisdiction, /police, /detention, /library, /hospital, /search, /ask, /brief | Gold standard, 33 commands, 3,800-city civic database |
| **Legal Documents** | lawclaw -> docuclaw | /doc, /draft | LawClaw enriches with jurisdiction + court rules, delegates to docuclaw |
| **Legal Translation** | lawclaw -> interpretclaw | /translate | Preserves Latin, French, citations, party names |
| **Medical Diagnosis** | mediclaw | /diagnose, /treatment, /medications, /warnings, /emergency, /pediatrics, /geriatrics | Groq-powered, 91 specialties, authoritative sourcing |
| **Hospital Geolocation** | mediclaw | /hospital, /nearest | Name, address, phone, website, GPS from 3,800+ city jurisdiction files via cached_search() |
| **Medical Research** | mediclaw | /research, /med, /referral | Medical references via WebClaw BM25 + Chronicle FTS5 |
| **Plotting/Charts** | plotclaw | /plot, /chart, /graph, /bar, /line, /scatter, /pie | 15 chart types |
| **Document Creation** | docuclaw | /create, /letter, /report, /memo, /resume, /proposal, /import, /export, /convert, /combine | 31 commands, cached_search() wired |
| **Flowcharts/Diagrams** | flowclaw | /flowchart, /mindmap, /sequence, /architecture | Mermaid.js rendering |
| **Code Generation** | claw_coder | /code, /debug, /review, /tutorial, /explain | 39 languages, cached_search() wired |
| **Rust Specialist** | crustyclaw | /rust, /audit, /pinch, /fix | Rust programming + audit |
| **Mathematics** | mathematicaclaw | /math, /solve, /derivative, /integral, /plot | SymPy + Plotly |
| **Translation** | interpretclaw | /translate, /detect, /speak | 42 languages |
| **Language Teaching** | langclaw | /lesson, /vocab, /practice, /teach | Memory-persisted lessons |
| **File Operations** | fileclaw | /import, /export, /convert | 41+ formats, universal file handler |
| **Web Search** | webclaw | search, fetch | BM25 retrieval, Chronicle FTS5, source confidence scoring |
| **Data Processing** | dataclaw | /search, /find, /export | Local data retrieval + WebClaw result cache storage |
| **Blockchain/TX** | txclaw | /tx, /network, /search, /contract, /staking, /gas, /governance | TX.org exclusive, 135 live URLs + 529 local files |
| **Model Management** | llmclaw | /use, /list, /models | Sovereign Gateway, 4 providers (groq/openrouter/anthropic/ollama) |
| **Model Liberation** | liberateclaw | /liberate, /obliterate, /models | Obliterated model management |
| **Technical Drawings** | draftclaw | /blueprint, /permit, /structural, /cad | Building permits, 4,744 jurisdiction entries |
| **Graphic Design** | designclaw | /brand, /colors, /logo, /kit | Brand identity design |
| **AI Drawing** | drawclaw | /draw, /paint, /sketch, /illustrate | 15 commands |
| **AI Vision** | dreamclaw | /dream, /imagine | AI vision generation |
| **Code Crawler** | rustypycraw | /crawl, /scan, /analyze | AST crawling |

## Retrieval Architecture

### Two Agent Classes (Discovered June 5, 2026)

**BM25 agents (9)**: Return raw retrieval with score/source/dedup markers.
lawclaw, claw_coder, crustyclaw, designclaw, dreamclaw, interpretclaw,
langclaw, liberateclaw, webclaw

**Non-search agents (12)**: Route retrieval through ask_llm() which strips
BM25 markers. Both paths WORK — just different output format.

### Retrieval Pipeline
```
User Query -> _gather_context() -> cached_search()
  -> DataClaw Cache -> (miss) WebClaw BM25 -> Chronicle FTS5
  -> final_score = bm25_score * source_weight
  -> Context -> ask_llm() -> Response
```

### DataClaw Cache
- agents/dataclaw/cache/{agent}/ — WebClaw result cache (24hr TTL)
- agents/dataclaw/references/{agent}/ — 21 agent directories created
- Only lawclaw actively populating cache (June 5)
- Target: all retrieval agents populate cache for local-first retrieval

## Delegation Patterns

### Simple Delegation (via capability registry)
Any agent can access any capability. The registry routes silently.

### Enriched Delegation (domain-specific routes)
- lawclaw -> docuclaw: adds jurisdiction + court rules
- mediclaw -> interpretclaw: preserves medical terminology
- claw_coder -> crustyclaw: Rust code audit

### Cached Delegation (automatic)
- BaseAgent.cached_search() — cache first, WebClaw fallback, cache write
- BaseAgent.call_agent() — cross-agent with circuit breaker

## Shared Infrastructure (All Agents)

| System | Purpose | Coverage |
|--------|---------|----------|
| Circuit breaker | 5 failures = 60s open circuit | All call_agent() |
| BM25 retrieval | Provider + Chronicle + dedup + source confidence | All cached_search() |
| Search cache | 24hr TTL via DataClaw | All cached_search() |
| Sovereignty enforcement | 6 patterns blocked at HTTP boundary (403) | All A2A requests |

## Constitutional Boundaries

- Article I: All LLM access through Sovereign Gateway only
- Article II: Each agent has defined jurisdiction. No crossing.
- Article III: All cross-agent routing uses BaseAgent.call_agent()
- Article VII: All exceptions must log. except: pass is UNCONSTITUTIONAL.
