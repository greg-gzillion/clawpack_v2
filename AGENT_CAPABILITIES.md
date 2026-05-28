
Agent Capability Map — Clawpack V2
The 21 Agents and Their Jurisdictions
#AgentJurisdictionDelegates To
1lawclawLaw research & analysisdocuclaw, webclaw, plotclaw, flowclaw
2flowclawFlowcharts & diagramsdocuclaw, webclaw, dataclaw, fileclaw
3docuclawDocument creation for ALL agentsfileclaw, interpretclaw
4mathematicaclawMath & computationdocuclaw, plotclaw
5liberateclawModel liberationSovereign Gateway
6txclawBlockchain & smart contractsdocuclaw, fileclaw
7interpretclawTranslation & speechwebclaw
8langclawLanguage learningwebclaw
9claw_coderCode generation (39 langs)webclaw, dataclaw, crustyclaw, docuclaw
10dataclawData processing & analysisfileclaw
11webclawWeb search & indexingChronicle
12fileclawFile operations (52 formats)docuclaw
13plotclawCharts & graphsdocuclaw
14mediclawMedical analysisdocuclaw, webclaw, dataclaw, lawclaw
15dreamclawAI vision & generationSovereign Gateway
16designclawGraphic designdocuclaw
17draftclawTechnical drawingsdocuclaw
18crustyclawRust AI assistantclaw_coder
19rustypycrawCode crawlerwebclaw, dataclaw, crustyclaw, claw_coder
20drawclawAI drawing & artdocuclaw
21llmclawModel managerSovereign Gateway
lawclaw Cross-Agent Connections
lawclaw → docuclaw
When: User runs /export or asks to create a document

How: delegate("docuclaw", f"/create {research_summary}", timeout=60)

Trigger: /export command in agent_handler.py

lawclaw → webclaw
When: Fetching live URLs, web search

How: webclaw(url) from _helpers.py

Rule: NEVER use requests.get() directly — always through webclaw A2A

lawclaw → plotclaw
When: Visualizing circuit splits, case timelines, jurisdiction maps

How: delegate("plotclaw", f"/plot {data}", timeout=30)

Trigger: /chart command in agent_handler.py

lawclaw → flowclaw
When: Legal procedure flows, court hierarchy diagrams

How: delegate("flowclaw", f"/flowchart {description}", timeout=30)

Trigger: /diagram command in agent_handler.py

Agents That Call lawclaw
mediclaw → lawclaw
When: Medical cases with legal dimensions (HIPAA, malpractice)

How: self.call_agent("lawclaw", f"search medical regulation {query}")

Status: ACTIVE — wired in mediclaw/agent_handler.py line 25

txclaw → lawclaw
When: Blockchain regulatory research

How: delegate("lawclaw", f"/statute {regulation}")

Status: Available, not yet wired

dataclaw → lawclaw
When: Legal data analysis needs jurisdiction context

How: delegate("lawclaw", f"/jurisdiction {location}")

Status: Available, not yet wired

Shared Infrastructure (All 21 Agents)
SystemPathPurpose
Chronicledata/chronicle.db (448MB)Full-text indexed audit trail
Unified Memorydata/memory_index.jsonFast keyword index for cross-agent recall
Sovereign Gatewayshared/llm/client.pyAll LLM calls route here
Truth Resolvershared/truth_resolver.pySource conflict resolution
Memory Guardshared/memory_guard.pyBlocks inference-tier, enforces 0.75 threshold
Agent Registryshared/registry.pyCanonical delegation map
Decision Ledgershared/decision_ledger.pyTamper-evident audit hash chain
Connection Status by Agent (May 2026)
AgentChronicleUnified MemoryCross-agent callsStatus
lawclawYESYES4Connected
claw_coderYESYES5Most outbound
flowclawYESNO5Connected
docuclawNONO4Connected
mediclawNONO4Connected
rustypycrawYESNO4Connected
draftclawNONO3Connected
plotclawNONO3Connected
txclawYESNO3Connected
webclawYESNO0Writes Chronicle
drawclawNONO0Isolated
fileclawNONO0Isolated
mathematicaclawNONO0Isolated
One-Session Connection Checklist
A2A_PROTOCOL.md — how agents call each other

SHARED_MEMORY_PROTOCOL.md — how agents learn together

AGENT_CAPABILITIES.md — this file

lawclaw → webclaw (via _helpers.webclaw())

lawclaw → docuclaw (/export in agent_handler.py)

lawclaw → plotclaw (/chart in agent_handler.py)

lawclaw → flowclaw (/diagram in agent_handler.py)

auto_delegate() + memory_write() in _helpers.py

/law + /precedent wired for memory + delegation

/state command

/statute command

/summarize command

Memory wired in remaining commands
