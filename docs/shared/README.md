# 🦞 CLAWPACK V2 - SHARED MODULE REFERENCE
## Foundation Library for All Agents

**Updated:** 2026-04-23

---

## Overview

The shared/ directory is the foundation library that ALL agents inherit from. It provides WebClaw search, LLM access, chronicle integration, memory, and state management through a single base class: BaseAgent.

---

## BaseAgent (shared/base_agent.py)

Every agent inherits from this class. It provides:

| Method | Purpose |
|--------|---------|
| search_web(query, max_results=5) | Search WebClaw SQLite index (1.5M terms, 20K files) |
| search_web_raw(query, max_results=10) | Search without content snippets |
| search_local(query) | Search DataClaw local index |
| sk_llm(prompt) | Call LLMClaw via A2A (Groq → Ollama → OpenRouter) |
| search_chronicle(query, limit=5) | Search chronicle ledger for URLs |
| ecord_in_chronicle(url, context, source) | Record URL in chronicle |
| learn(key, value) | Store agent state |
| ecall(key) | Retrieve agent state |
| learn_fact(fact) | Store shared fact |
| get_facts() | Get all shared facts |
| 	rack_interaction() | Increment interaction counter |
| get_stats() | Get agent statistics |
| handle(task) | Override in subclass — returns dict |

### Agent Handler Template

`python
"""A2A Handler for [AgentName]"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.base_agent import BaseAgent

class ExampleAgent(BaseAgent):
    def __init__(self):
        super().__init__('example')

    def handle(self, task: str) -> dict:
        self.track_interaction()
        # Parse command and args
        # Call self.ask_llm() or self.search_web()
        # Return {"status": "success", "result": "..."}

_agent = ExampleAgent()

def process_task(task: str, agent: str = None):
    return _agent.handle(task)
Three-Tier Memory (shared/memory/)
TierFilePurpose
Working Memorythree_tier.pyCurrent conversation context
Semantic Memorythree_tier.pyFacts and knowledge
Procedural Memoryprocedural_memory.pyRules with confidence decay
LLM Integration (shared/llm/)
FilePurpose
client.pyAsync LLM client (Groq, Anthropic, OpenAI, OpenRouter, Ollama)
manager.pyProvider management from working_llms.json and active_model.json
streaming.pyStreaming LLM responses
webclaw.pyWebClaw provider integration
anthropic.pyAnthropic API provider
ollama.pyOllama local provider
openrouter.pyOpenRouter API provider
How It Connects
text
A2A Server
    │
    ├── imports agent_handler.py
    │       └── extends BaseAgent (shared/base_agent.py)
    │               ├── search_web() → WebclawProvider → SQLite (1.5M terms)
    │               ├── ask_llm() → LLMClaw → Groq/Ollama/OpenRouter
    │               ├── search_chronicle() → Chronicle Ledger
    │               └── learn/recall → Shared Memory
    │
    └── Three-Tier Memory (shared/memory/)
Current Connected Agents
AgentUses BaseAgentHandler
webclaw❌ (custom)agent_handler.py
llmclaw❌ (custom)agent_handler.py
lawclaw❌ (custom)agent_handler.py
mediclaw❌ (custom)agent_handler.py
mathematicaclaw❌ (custom)agent_handler.py
claw_coder❌ (custom)agent_handler.py
crustyclaw✅agent_handler.py
All agents should be migrated to use BaseAgent pattern.
