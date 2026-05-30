# AGENT_CAPABILITIES.md — Constitutional Capability Registry

## Capability-to-Agent Mapping

Every capability has exactly one constitutional owner. This prevents jurisdiction conflicts.

| Capability | Constitutional Owner | Key Commands | Notes |
|-----------|---------------------|----------|-------|
| **Legal Research** | lawclaw | /law, /docket, /cite, /precedent, /oral, /statute, /summarize, /federal, /state, /court, /judge, /jurisdiction, /police, /detention, /library, /hospital, /list, /browse, /search, /analyze, /ask, /brief | Gold standard, 24 commands, 3,800-city civic database |
| **Legal Documents** | lawclaw -> docuclaw | /doc, /draft | LawClaw enriches with jurisdiction + court rules, delegates to docuclaw |
| **Legal Translation** | lawclaw -> interpretclaw -> docuclaw | /translate | Preserves Latin, French, citations, party names. Chains through docuclaw |
| **Fact Correction** | lawclaw | /correct | Community corrections via consensus engine |
| **Medical Diagnosis** | mediclaw | /diagnose, /treatment, /research, /med, /referral | Professional/layperson detection, urgency triage, hospital routing |
| **Emergency Medicine** | mediclaw | /emergency, /er, /nearest | Auto ER lookup with GPS coordinates from 3,800+ cities |
| **Hospital Geolocation** | mediclaw | /hospital, /specialty, /nearest | Find by city, specialty (cardiac/pediatric/trauma/etc.), or GPS |
| **Medical Documents** | mediclaw -> docuclaw | /doc medical report, /doc referral letter, /doc treatment plan, /doc discharge | Medical term preservation in translation chain |
| **Plotting/Charts** | plotclaw | /plot, /chart, /graph, /bar, /line, /scatter, /pie, /hist, /heatmap, /polar, /surface, /box, /compare, /dashboard, /stats | 15 chart types, smart title/axis extraction |
| **Document Creation** | docuclaw | /create, /letter, /report, /memo, /resume, /proposal, /import, /export, /convert, /combine | 31 commands, validation engine, multi-format export |
| **Flowcharts/Diagrams** | flowclaw | /flow, /flowchart, /diagram, /mindmap, /sequence, /architecture | Mermaid.js, browser rendering, multi-format export |
| **Code Generation** | claw_coder | /code, /debug, /review, /tutorial, /explain, /run, /test, /scan, /translate | 39 languages, memory recall before generation |
| **Rust Audit** | crustyclaw | /rust, /audit, /pinch, /fix, /test, /cargo, /run | Standalone binary fallback, memory-persisted findings |
| **Mathematics** | mathematicaclaw | /math, /solve, /derivative, /integral, /plot, /animate, /add, /algebra, /calculus | SymPy + Plotly, 9 commands |
| **Translation** | interpretclaw | /translate, /detect, /languages, /speak, /braille | 42 languages (incl. Latin, ASL gloss), cross-platform TTS, Braille (opt-in) |
| **Language Teaching** | langclaw | /lesson, /vocab, /practice, /speak, /teach, /conversation | Cross-platform TTS, memory-persisted lessons |
| **File Operations** | fileclaw | /import, /export, /convert | 41+ formats, universal file handler for all agents |
| **Web Search** | webclaw | search, fetch | Chronicle-indexed, 35,000+ entries, 3,800-city references |
| **Data Processing** | dataclaw | /search, /find, /export, /index | 41,000+ local files, Chronicle writes, search cache |
| **Blockchain/TX** | txclaw | /tx, /network, /search, /contract | TX Blockchain, smart contracts |
| **Model Management** | llmclaw | /llm, /use, /list, /normal, /obliterated | Sovereign Gateway orchestration, 4 providers, 17 models |
| **Model Liberation** | liberateclaw | /liberate, /obliterate, /models, /use | Obliterated model management |
| **Technical Drawings** | draftclaw | /blueprint, /permit, /structural, /cad, /lookup, /correct | Building permits, design criteria, 4,744 jurisdiction entries |
| **Graphic Design** | designclaw | /brand, /colors, /mood, /type, /copy, /logo, /kit, /html, /buildingcodes | Brand identity, building code lookup from jurisdiction files |
| **AI Drawing** | drawclaw | /draw, /paint, /sketch, /illustrate, /cartoon, /doodle, /animate, /canvas, /compose, /describe, /filter, /prompt, /qrcode, /style, /library | 15 commands, library resource lookup |
| **AI Vision** | dreamclaw | /dream, /imagine | AI vision generation |
| **Code Crawler** | rustypycraw | /crawl, /scan, /analyze | AST crawling, delegates to claw_coder + crustyclaw |

## Delegation Patterns

### Simple Delegation (via capability registry)
Any agent can access any capability. The registry routes silently.
Example: `/plot` in lawclaw → capability registry → plotclaw

### Enriched Delegation (domain-specific routes)
Agents add domain expertise before delegating:
- lawclaw `/doc` → adds jurisdiction + court rules → docuclaw
- lawclaw `/translate` → adds legal term preservation → interpretclaw → docuclaw
- mediclaw `/translate` → adds medical term preservation → interpretclaw → docuclaw
- mediclaw `/diagnose` → adds hospital routing from 3,800+ cities
- claw_coder `/code rust` → calls crustyclaw `/audit` for best practices

### Chain Delegation (multi-agent pipelines)
- `/doc` → lawclaw enriches → docuclaw creates → exports/
- `/translate` → preserves terms → interpretclaw translates → docuclaw formats → exports/
- `/diagnose` → mediclaw analyzes → webclaw enriches → hospital lookup → response

### Cached Delegation (automatic)
- `BaseAgent.cached_search()` — web searches cached via DataClaw, 24hr TTL
- `BaseAgent.lookup_jurisdiction()` — Chronicle FTS5 lookup for all 21 agents

## Shared Infrastructure (All Agents)

| System | Purpose | Coverage |
|--------|---------|----------|
| Circuit breaker | 5 failures = 60s open circuit | All call_agent() |
| Task state machine | pending → running → completed/failed/killed | All call_agent() |
| Memory staleness | Age warnings on facts >24hr old | All _memory.recall() |
| Search cache | 24hr TTL via DataClaw | All cached_search() |
| Jurisdiction lookup | Library, hospital, police, building codes | All lookup_jurisdiction() |
| 36-system boundary | Input validation, permissions, gates, config, etc. | 19/21 agents |

## Constitutional Boundaries

- Article II: Each agent has defined jurisdiction. No crossing.
- Article III: All cross-agent routing uses BaseAgent.call_agent()
- Capability registry preserves Article II — agents recognize foreign capabilities and delegate
- Domain enrichment is constitutional — adding expertise before delegation
