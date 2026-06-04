# READ THIS FIRST - Clawpack V2

## Quick Start (5 minutes)
1. python scripts/scan.py          # System health check
2. python scripts/onboard.py        # Full documentation (run once, read output)

## Essential Files (read in this order)
1. shared/base_agent.py             # Foundation class for all 21 agents
2. shared/llm/client.py             # Sovereign Gateway - all LLM access
3. agents/webclaw/providers/webclaw_provider.py  # Central retrieval layer
4. agents/lawclaw/agent_handler.py  # Reference implementation (gold standard)
5. CLAWPACK_ONBOARD.md              # Architecture, rules, session log
6. docs/KNOWN_TRAPS.md              # Mistakes that cost hours - read before coding

## How to verify your changes
- Changed WebClaw?    python scripts/test_functional.py
- Changed Gateway?    python scripts/test_fallback_chain.py
- Changed an agent?   python scripts/test_all_agents.py
- Cross-agent?        python scripts/test_interagent.py

## Critical architecture rules
- All LLM -> shared/llm/client.py (Sovereign Gateway, Article I)
- All search -> namespace-scoped (ns:{agent} prefix required)
- All deployment -> command files only (never inject into handlers)
- All exceptions -> must log (except: pass is UNCONSTITUTIONAL)

## Current state (June 4, 2026)
- Version: 3.2.0
- Phase: Late Alpha / Beta Candidate
- Agents: 21/21 operational
- Providers: ollama, groq, direct_model, openrouter
- Active model: gemma3:4b (Ollama, 3.3GB GPU)
- Beta gates: 5/10 complete
- Next: FlowClaw consolidation, security review, clean install testing
