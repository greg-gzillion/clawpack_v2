# Agent Capability Map - Clawpack V2

## The 21 Agents and Their Jurisdictions

| # | Agent | Jurisdiction | Delegates To |
|---|-------|-------------|-------------|
| 1 | lawclaw | Law research and analysis | docuclaw, webclaw, plotclaw, flowclaw |
| 2 | flowclaw | Flowcharts and diagrams | docuclaw, webclaw, dataclaw, fileclaw |
| 3 | docuclaw | Document creation for ALL agents | fileclaw, interpretclaw |
| 4 | mathematicaclaw | Math and computation | docuclaw, plotclaw |
| 5 | liberateclaw | Model liberation | Sovereign Gateway |
| 6 | txclaw | Blockchain and smart contracts | docuclaw, fileclaw |
| 7 | interpretclaw | Translation and speech | webclaw |
| 8 | langclaw | Language learning | webclaw |
| 9 | claw_coder | Code generation (39 langs) | webclaw, dataclaw, crustyclaw, docuclaw |
| 10 | dataclaw | Data processing and analysis | fileclaw |
| 11 | webclaw | Web search and indexing | Chronicle |
| 12 | fileclaw | File operations (52 formats) | docuclaw |
| 13 | plotclaw | Charts and graphs | docuclaw |
| 14 | mediclaw | Medical analysis | docuclaw, webclaw, dataclaw, lawclaw |
| 15 | dreamclaw | AI vision and generation | Sovereign Gateway |
| 16 | designclaw | Graphic design | docuclaw |
| 17 | draftclaw | Technical drawings | docuclaw |
| 18 | crustyclaw | Rust AI assistant | claw_coder |
| 19 | rustypycraw | Code crawler | webclaw, dataclaw, crustyclaw, claw_coder |
| 20 | drawclaw | AI drawing and art | docuclaw |
| 21 | llmclaw | Model manager | Sovereign Gateway |

## lawclaw Cross-Agent Connections

### lawclaw to docuclaw
- When: User runs /export or asks to create a document
- How: delegate("docuclaw", f"/create {research_summary}", timeout=60)

### lawclaw to webclaw
- When: Fetching live URLs, web search
- How: webclaw(url) from _helpers.py
- Rule: NEVER use requests.get() directly

### lawclaw to plotclaw
- When: Visualizing circuit splits, case timelines
- How: delegate("plotclaw", f"/plot {data}", timeout=30)

### lawclaw to flowclaw
- When: Legal procedure flows, court hierarchy diagrams
- How: delegate("flowclaw", f"/flowchart {description}", timeout=30)

## Agents That Call lawclaw

### mediclaw to lawclaw
- When: Medical cases with legal dimensions (HIPAA, malpractice)
- Status: ACTIVE - wired in mediclaw/agent_handler.py

### txclaw to lawclaw (available)
- When: Blockchain regulatory research

### dataclaw to lawclaw (available)
- When: Legal data analysis needs jurisdiction context

## Shared Infrastructure (All 21 Agents)

| System | Path | Purpose |
|--------|------|---------|
| Chronicle | data/chronicle.db (448MB) | Full-text indexed audit trail |
| Unified Memory | data/memory_index.json | Fast keyword index for cross-agent recall |
| Sovereign Gateway | shared/llm/client.py | All LLM calls route here |
| Truth Resolver | shared/truth_resolver.py | Source conflict resolution |
| Memory Guard | shared/memory_guard.py | Blocks inference-tier, enforces 0.75 threshold |
| Agent Registry | shared/registry.py | Canonical delegation map |
| Decision Ledger | shared/decision_ledger.py | Tamper-evident audit hash chain |
| Agent Helpers | shared/_agent_helpers.py | Empire-wide utilities (all 21 agents) |

## Connection Status by Agent (May 28, 2026)

All 21 agents now import shared/_agent_helpers.py for constitutional audit logging.
All 21 agents inherit from BaseAgent with call_agent(), ask_llm(), search_chronicle().
No isolated agents remain - every agent has cross-agent communication capability.

## One-Session Connection Checklist

- [x] A2A_PROTOCOL.md
- [x] SHARED_MEMORY_PROTOCOL.md
- [x] AGENT_CAPABILITIES.md (this file)
- [x] All 21 agents wired with _agent_helpers
- [x] All 12 lawclaw commands complete
- [x] 4 civic commands added (/police, /detention, /library, /hospital)
- [x] _helpers.py for lawclaw shared utilities
- [x] _memory.py for cross-command shared learning
- [x] auto_delegate() + memory_write() in _helpers.py
- [x] /export, /chart, /diagram delegation routes in agent_handler.py
- [x] Root documentation cleaned up
- [ ] Shared memory wired into all lawclaw commands
- [ ] Enforcement engine activated in a2a_server.py
- [ ] Decision ledger wired into BaseAgent
