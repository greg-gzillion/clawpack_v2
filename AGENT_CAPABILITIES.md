# AGENT_CAPABILITIES.md — Constitutional Capability Registry

## Capability-to-Agent Mapping

Every capability has exactly one constitutional owner. This prevents jurisdiction conflicts.

| Capability | Constitutional Owner | Commands | Notes |
|-----------|---------------------|----------|-------|
| **Legal Research** | lawclaw | /law, /docket, /cite, /precedent, /oral, /statute, /summarize, /federal, /state, /court, /judge, /jurisdiction, /police, /detention, /library, /hospital, /list, /browse, /search, /analyze, /ask, /brief | Gold standard reference implementation |
| **Legal Documents** | lawclaw -> docuclaw | /doc, /draft | LawClaw enriches with jurisdiction data, delegates to docuclaw |
| **Legal Translation** | lawclaw -> interpretclaw -> docuclaw | /translate | Preserves Latin, French, citations, party names. Chains through docuclaw for formatting |
| **Fact Correction** | lawclaw | /correct | Community corrections via consensus engine |
| **Plotting/Charts** | plotclaw | /plot, /chart, /graph, /bar, /line, /scatter, /pie, /hist, /heatmap, /polar, /surface, /box, /compare, /dashboard, /stats | 13 chart types |
| **Document Creation** | docuclaw | /create, /letter, /report, /memo, /resume, /proposal, /import, /export, /convert, /combine | 31 commands, 21 format exports |
| **Flowcharts/Diagrams** | flowclaw | /flow, /flowchart, /diagram, /mindmap | Architecture, sequences, flowcharts |
| **Code Generation** | claw_coder | /code, /debug, /review, /docs, /test, /translate, /explain, /perf, /project, /tutorial | 39 languages |
| **Mathematics** | mathematicaclaw | /math, /solve, /derivative, /integral, /limit, /plot, /animate | SymPy + Plotly |
| **Translation (Generic)** | interpretclaw | /translate, /detect, /languages, /speak, /listen, /translatedoc, /vocab, /lesson | 39 languages |
| **Language Teaching** | langclaw | /lesson, /vocab, /practice, /speak, /teach, /conversation | Interactive language learning |
| **File Operations** | fileclaw | /export, /convert, /import | 52 formats |
| **Web Search** | webclaw | /search, /fetch | Chronicle-indexed, 76K+ entries |
| **Data Processing** | dataclaw | /search, /data | Local file search + Chronicle |
| **Blockchain/TX** | txclaw | /tx, /network, /search, /contract | TX Blockchain |
| **Medical Analysis** | mediclaw | /diagnose, /treatment, /medications, /research, /sources | 91 specialties |
| **Model Management** | llmclaw | /llm, /orchestrate, /models, /use, /obliterated, /normal | Sovereign Gateway |
| **Model Liberation** | liberateclaw | /liberate, /obliterate, /models, /use | Obliterated model management |
| **Technical Drawings** | draftclaw | /blueprint, /permit, /structural, /cad, /lookup, /correct | Building permits, blueprints |
| **Graphic Design** | designclaw | /brand, /colors, /mood, /type, /copy, /logo, /kit, /html | Brand identity, HTML generation |
| **AI Drawing** | drawclaw | /draw, /paint, /sketch, /illustrate, /cartoon, /doodle, /animate, /canvas, /compose, /describe, /filter, /prompt, /qrcode, /style | 15 commands |
| **AI Vision** | dreamclaw | /dream | AI vision and generation |
| **Rust AI** | crustyclaw | /rust, /explain, /audit, /pinch, /fix, /test, /cargo, /run | Rust compiler validation |
| **Code Crawler** | rustypycraw | /crawl, /scan, /analyze | AST crawling, code scanning |

## Delegation Patterns

### Simple Delegation (via capability registry)
Any agent can access any capability. The registry routes silently.
Example: User types /plot in lawclaw -> capability registry -> plotclaw

### Enriched Delegation (domain-specific routes)
Some agents add domain expertise before delegating.
Example: /doc in lawclaw adds jurisdiction context before calling docuclaw
Example: /translate in lawclaw adds legal term preservation before calling interpretclaw

### Chain Delegation (multi-agent pipelines)
Complex workflows chain through multiple agents.
Example: /doc -> lawclaw enriches -> docuclaw creates -> exports/
Example: /translate -> lawclaw preserves terms -> interpretclaw translates -> docuclaw formats -> exports/

## Constitutional Boundaries

- Article II: Each agent has defined jurisdiction. No crossing.
- Article III: All cross-agent routing uses BaseAgent.call_agent()
- Capability registry preserves Article II — agents recognize foreign capabilities and delegate
- Domain enrichment is constitutional — adding expertise before delegation, not performing another agent's function
