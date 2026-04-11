# Attribution: Liu Juanjuan Inspired Features

## Overview
This document acknowledges the profound influence of Liu Juanjuan's (@liujuanjuan1984) open-source projects on the development of Clawpack v2.0's advanced features.

## Inspired Projects & Implementations

### 1. Common Chronicle → Chronicle Timeline
**Source**: https://github.com/Intelligent-Internet/Common_Chronicle
**Concept**: "Turning messy context into structured, sourced timelines"
**Clawpack Implementation**: 
- Structured timeline queries in WebClaw chronicle
- Source-attributed context retrieval
- Temporal organization of indexed cards

### 2. cass-memory → Procedural Memory & Trauma Guard
**Source**: https://github.com/Dicklesworthstone/cass_memory_system
**Implemented Features**:
- Procedural memory with confidence decay (90-day half-life)
- 4x harmful multiplier for negative feedback
- Anti-pattern conversion from harmful rules
- Maturity states: candidate → established → proven
- Trauma Guard safety system blocking dangerous commands
- Pattern-based dangerous operation detection

### 3. codex-a2a → A2A Protocol
**Source**: https://github.com/liujuanjuan1984/codex-a2a
**Implemented Features**:
- A2A protocol server on port 8765
- Agent discovery via `/.well-known/agent.json`
- Message routing and agent-to-agent communication
- A2A-compliant endpoints for inter-agent messaging

### 4. rustclaw → Lifecycle Hooks
**Source**: https://github.com/liujuanjuan1984/rustclaw
**Implemented Features**:
- Hook points: BEFORE_INBOUND, BEFORE_TOOL_CALL, BEFORE_OUTBOUND
- ON_SESSION_START, ON_SESSION_END lifecycle events
- TransformResponse for output modification

### 5. a2a-client-hub → Session Continuity
**Source**: https://github.com/liujuanjuan1984/a2a-client-hub
**Implemented Features**:
- Persistent session management across agent restarts
- Message history storage and retrieval
- Session summarization and continuity

## Key Principles Adopted

From Liu Juanjuan's work, we adopted:
1. **Structured Context** - Raw data becomes knowledge when organized
2. **Source Attribution** - Every piece of information needs verification
3. **Temporal Organization** - Timeline-based structuring for understanding
4. **Confidence Decay** - Knowledge fades without reinforcement
5. **Anti-Pattern Learning** - Bad rules become warnings
6. **Safety First** - Prevent catastrophic operations before execution
7. **Agent Discovery** - A2A protocol for inter-agent communication

## Implementation Files

| Feature | Files |
|---------|-------|
| Timeline | `agents/webclaw/core/chronicle_ledger.py` |
| Procedural Memory | `agents/shared/memory/procedural_memory.py` |
| Trauma Guard | `agents/shared/safety/trauma_guard.py` |
| A2A Server | `a2a_server.py` |
| Hooks | `agents/claw_coder/hooks.py` |
| Session Manager | `agents/docuclaw/session/session_manager.py` |

## Thank You

Deepest gratitude to Liu Juanjuan for sharing his insights openly. His work on:
- Common Chronicle (structured timelines)
- cass-memory (procedural memory for AI agents)
- codex-a2a (A2A protocol implementation)
- rustclaw (hook systems)
- a2a-client-hub (session continuity)

...directly shaped these features in Clawpack v2.0.

> *"试着用自己的语言复述一些基础常识"* - Liu Juanjuan
> *(Try to restate basic common sense in your own words)*

We've tried to do exactly that.

---

**致敬开源精神，致敬知识分享者**
