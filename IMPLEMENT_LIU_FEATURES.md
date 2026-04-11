# Features to Implement from Liu Juanjuan's Projects

## 1. Timeline Structuring (Common Chronicle)
File: agents/webclaw/core/chronicle_ledger.py

Add these methods:
- create_timeline(topic) - returns structured timeline
- get_sourced_context(query) - returns context with source attribution

## 2. Procedural Memory (cass-memory)
File: agents/shared/memory/procedural_memory.py

Features:
- Rules with confidence scoring
- 90-day half-life decay
- 4x harmful multiplier
- Anti-pattern conversion
- Maturity states: candidate → established → proven

## 3. A2A Protocol (codex-a2a)
File: agents/webclaw/a2a_server.py

Endpoints:
- /.well-known/agent.json - agent discovery
- /v1/message - message handling
- /v1/stream - streaming responses

## 4. Lifecycle Hooks (rustclaw)
File: agents/claw_coder/hooks.py

Hook points:
- BEFORE_INBOUND / BEFORE_TOOL_CALL / BEFORE_OUTBOUND
- ON_SESSION_START / ON_SESSION_END
- TRANSFORM_RESPONSE

## 5. Session Continuity (a2a-client-hub)
File: agents/docuclaw/session_manager.py

Features:
- Persistent sessions across runs
- Message history
- Session summaries

## 6. Trauma Guard Safety (cass-memory)
File: agents/shared/safety/trauma_guard.py

Patterns:
- rm -rf / → FATAL
- DROP DATABASE → FATAL
- git push --force → HIGH
- chmod 777 → MEDIUM

## Status: Ready for implementation
