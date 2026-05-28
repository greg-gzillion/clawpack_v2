# LLMClaw — Model Manager & Sovereign Gateway

21-agent ecosystem member. A2A on port 8766. Constitutional governance.

## What LLMClaw Does
Model selection, provider switching, multi-agent orchestration, and the
Sovereign Gateway that all 21 agents route LLM calls through.

## Commands

- `/llm [prompt]` — Direct inference through Sovereign Gateway
- `/orchestrate [query]` — Multi-agent orchestration (auto-delegates to specialists)
- `/models` — List all 25 available models (obliterated + standard)
- `/use [model]` — Switch active model system-wide
- `/obliterated` — List obliterated (liberated) models only
- `/normal` — List standard (non-obliterated) models
- `/help` — Command reference
- `/stats` — System statistics

## Architecture

### Sovereign Gateway
All model access routes through LLMClaw. No agent speaks to a model directly.
4 providers: Ollama (local) · Groq · OpenRouter · Anthropic

### Multi-Agent Orchestration
The `/orchestrate` command intelligently routes queries to the right agents:
- mediclaw for medical queries
- lawclaw for legal research
- webclaw for web search
- dataclaw for local file search
- claw_coder for code generation
- And 16 more specialists

### Model Management
25 models available across 4 providers. 5 obliterated models for sovereign
local execution. Provider switching via `/use` command.

## Key Files
- `agent_handler.py` — A2A handler, orchestration engine, model switching
- `commands/llm.py` — Direct LLM inference
- `commands/use.py` — Model switching
- `llmclaw.py` — CLI interface

## Constitution Compliance
- Sovereign Gateway: all model access routes through LLMClaw
- Provider governance: no agent selects its own provider
- Budget enforcement: daily budget tracked
- Audit logging: all LLM calls logged to Chronicle