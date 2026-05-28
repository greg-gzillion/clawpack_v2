# A2A Communication Protocol — Clawpack V2

## How Agents Talk to Each Other

All agent-to-agent communication routes through the A2A server on port 8766.
The constitutional path is `BaseAgent.call_agent()` inherited by every agent.

## Calling Another Agent

### From any lawclaw command (via _helpers.py):
```python
from agents.lawclaw.commands._helpers import delegate
result = delegate("docuclaw", "/create legal brief: {content}", timeout=60)
result = delegate("plotclaw", "/plot circuit split: {data}", timeout=30)
result = delegate("webclaw", "fetch https://...", timeout=20)
From any agent handler (via BaseAgent):
python
result = self.call_agent("webclaw", f"search {query}", timeout=15)
result = self.call_agent("docuclaw", f"/create {content}", timeout=60)
What Each Agent Accepts
AgentCommandReturns
docuclaw/create [content]document path
plotclaw/plot [data]chart
webclawfetch [url]page content
webclawsearch [query]search results
dataclawsearch [query]local file results
flowclaw/flowchart [desc]diagram
mediclaw/med [query]medical analysis
claw_coder/code [task]generated code file
fileclaw/export [fmt] [content]exported file path
interpretclaw/translate [text] to [lang]translated text
lawclaw/law [topic]legal research
lawclaw/docket [case]docket entries
lawclaw/jurisdiction [location]civic profile
Response Format
All agents return the same format:

json
{"status": "success"|"error", "result": "string content"}
Extract with:

python
resp.json().get("result", "")
Connection Status (May 2026)
AgentOutbound callsConnected to
claw_coder5webclaw, dataclaw, crustyclaw, + 14 via /delegate
flowclaw5webclaw, dataclaw, fileclaw, + 14 via /delegate
docuclaw4fileclaw, interpretclaw, + 14 via /delegate
mediclaw4webclaw, dataclaw, lawclaw, fileclaw
rustypycraw4webclaw, dataclaw, crustyclaw, claw_coder
lawclaw3webclaw, docuclaw, plotclaw, flowclaw
draftclaw3docuclaw
plotclaw3docuclaw
txclaw3docuclaw, fileclaw
drawclaw0isolated
fileclaw0isolated
mathematicaclaw0isolated
webclaw0writes to Chronicle
Adding a New Connection
Agent must inherit from BaseAgent (all 21 do)

Use self.call_agent(target, task, timeout) in handler

Or use delegate(target, task, timeout) from _helpers.py in commands

Document in AGENT_CAPABILITIES.md
