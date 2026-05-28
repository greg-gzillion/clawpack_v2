# A2A Communication Protocol - Clawpack V2

## How Agents Talk to Each Other

All agent-to-agent communication routes through the A2A server on port 8766.
The constitutional path is BaseAgent.call_agent() inherited by every agent.

## Calling Another Agent

### From any agent handler (via BaseAgent):
result = self.call_agent("webclaw", f"search {query}", timeout=15)
result = self.call_agent("docuclaw", f"/create {content}", timeout=60)

### From any command (via shared/_agent_helpers.py):
from shared._agent_helpers import delegate
result = delegate("myclaw", "docuclaw", "/create legal brief: {content}", timeout=60)

### Empire-wide helper (all 21 agents import this):
from shared._agent_helpers import delegate, llm, chronicle, log_err

## What Each Agent Accepts

| Agent | Command | Returns |
|-------|---------|---------|
| docuclaw | /create [content] | document path |
| plotclaw | /plot [data] | chart |
| webclaw | fetch [url] | page content |
| webclaw | search [query] | search results |
| dataclaw | search [query] | local file results |
| flowclaw | /flowchart [desc] | diagram |
| mediclaw | /med [query] | medical analysis |
| claw_coder | /code [task] | generated code file |
| fileclaw | /export [fmt] [content] | exported file path |
| interpretclaw | /translate [text] to [lang] | translated text |
| lawclaw | /law [topic] | legal research |
| lawclaw | /docket [case] | docket entries |
| lawclaw | /jurisdiction [location] | civic profile |

## Response Format

All agents return the same format:
{"status": "success"|"error", "result": "string content"}

Extract with:
resp.json().get("result", "")

## Connection Status (May 28, 2026)

All 21 agents inherit from BaseAgent. All 21 agents import shared/_agent_helpers.py.
Cross-agent delegation available empire-wide via call_agent() and delegate().
Constitutional audit logging (log_err) active on all agents.

Key outbound connections:
- claw_coder: webclaw, dataclaw, crustyclaw + 14 via /delegate
- flowclaw: webclaw, dataclaw, fileclaw + 14 via /delegate
- docuclaw: fileclaw, interpretclaw + 14 via /delegate
- mediclaw: webclaw, dataclaw, lawclaw, fileclaw
- rustypycraw: webclaw, dataclaw, crustyclaw, claw_coder
- lawclaw: webclaw, docuclaw, plotclaw, flowclaw

## Adding a New Connection

1. Agent must inherit from BaseAgent (all 21 do)
2. Use self.call_agent(target, task, timeout) in handler
3. Or use delegate(agent_name, target, task, timeout) from _agent_helpers
4. Document in AGENT_CAPABILITIES.md
