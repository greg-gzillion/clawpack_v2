# A2A Communication Protocol — Clawpack V2

## How Agents Talk to Each Other

All agent-to-agent communication routes through the A2A server on port 8766.
The constitutional path is `BaseAgent.call_agent()` — inherited by all 21 agents,
protected by circuit breaker (5 failures = 60s open circuit), and tracked by
the task state machine (pending → running → completed/failed/killed).

## Calling Another Agent

### From any agent handler (via BaseAgent):
```python
result = self.call_agent("webclaw", f"search {query}", timeout=15)
result = self.call_agent("docuclaw", f"/create {content}", timeout=60)
From any command (pass agent=self from handler):
python
def run(args, agent=None):
    result = agent.call_agent("plotclaw", f"/bar {data}", timeout=30)
    context = agent.ask_llm(prompt)  # Sovereign Gateway
    chronicle_results = agent.search_chronicle(query, limit=5)
    hospitals = agent.lookup_jurisdiction("Denver CO", "hospital")
Cached search (automatic 24hr cache via DataClaw):
python
result = self.cached_search("qualified immunity", timeout=15)
# First call: hits webclaw, caches result
# Subsequent calls within 24hr: returns cached result (zero tokens)
Communication Paths
1. Capability Registry (Automatic)
Unrecognized commands auto-route to the correct agent via shared/capabilities.py.
Any agent can type /plot data and it silently routes to plotclaw.

2. Direct Delegation (Explicit)
python
/delegate plotclaw /bar Q1 45 Q2 62 Q3 58 Q4 71
3. Enriched Delegation (Domain-Specific)
Agents add domain expertise before delegating:

lawclaw /doc → enriches with jurisdiction data → docuclaw

lawclaw /translate → adds legal term preservation → interpretclaw → docuclaw

mediclaw /translate → adds medical term preservation → interpretclaw → docuclaw

claw_coder /code rust → calls crustclaw /audit for best practices

Response Format
All agents return:

json
{"status": "success"|"error", "result": "string content"}
What Each Agent Accepts
AgentCommandsReturns
docuclaw/create [content]Formatted document
plotclaw/bar, /pie, /plot, /scatter, /hist, 9 moreChart PNG
webclawfetch [url], search [query]Page content / search results
dataclaw/search [query], /export [fmt] [query]Local file results
flowclaw/flowchart, /sequence, /architecture, /mindmapMermaid diagram
mediclaw/diagnose, /emergency, /er, /hospital, /specialty, /doc, /referralMedical analysis + hospital routing
claw_coder/code, /explain, /debug, /review, /tutorialGenerated code
crustyclaw/rust, /audit, /pinch, /fix, /test, /cargoRust audit/analysis
fileclaw/import [path], /export [fmt] [content], /convertFile operations
interpretclaw/translate [text] to [lang], /detect, /braille, /speakTranslation (42 languages)
langclaw/lesson, /vocab, /practice, /teach, /speakLanguage teaching
lawclaw/law, /docket, /jurisdiction, /doc, /translate, 18 moreLegal research + documents
mathematicaclaw/solve, /plot, /math, /calculusMath solutions
designclaw/brand, /logo, /colors, /kit, /buildingcodesBrand identity + building codes
draftclaw/structural, /permit, /blueprint, /cad, /lookupTechnical drawings
drawclaw/draw, /sketch, /paint, /illustrate, /libraryArt prompts + resources
dreamclaw/dream, /imagineAI vision prompts
liberateclaw/models, /liberated, /obliterate, /useModel management
llmclaw/llm, /use, /list, /normal, /obliteratedModel orchestration
txclawBlockchain commandsTX operations
rustypycraw/crawl, /scan, /analyzeCode analysis
Connection Status (May 29, 2026 — EVENING)
11 agents fully constitutional (10/10 audit score):
lawclaw, claw_coder, crustyclaw, designclaw, mediclaw, draftclaw, dreamclaw,
interpretclaw, langclaw, liberateclaw, dataclaw

9 agents partially connected (boundary + routing active, audit cosmetic gaps):
docuclaw, drawclaw, fileclaw, flowclaw, llmclaw, mathematicaclaw, plotclaw,
rustypycraw, txclaw, webclaw

All agents share:

23-system constitutional boundary (36 shared systems)

Circuit breaker on all cross-agent calls

Task state machine (pending → running → completed/failed/killed)

Chronicle FTS5 jurisdiction lookup via BaseAgent.lookup_jurisdiction()

Memory staleness warnings on facts older than 24 hours

Search result caching via DataClaw (24hr TTL)

Adding a New Connection
Agent must inherit from BaseAgent (all 21 do)

Use self.call_agent(target, task, timeout) for cross-agent calls

Use self.cached_search(query, timeout) for cached web searches

Use self.ask_llm(prompt) for Sovereign Gateway access

Use self.lookup_jurisdiction(city_state, type) for civic data
