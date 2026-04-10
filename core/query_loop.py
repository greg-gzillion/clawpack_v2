"""Query Loop - Async generator pattern for agent execution"""
import asyncio
from typing import AsyncGenerator, Dict, Any
from enum import Enum

class TerminalState(Enum):
    COMPLETED = "completed"
    USER_ABORT = "user_abort"
    MAX_TURNS = "max_turns"
    ERROR = "error"

class QueryLoop:
    """Async generator that is the heartbeat of the agent"""
    
    def __init__(self, agent_name: str, tools: Dict[str, Any]):
        self.agent_name = agent_name
        self.tools = tools
        self.message_history = []
        self.turn_count = 0
    
    async def run(self, prompt: str) -> AsyncGenerator[Dict, None]:
        """Generator yields messages, tool calls, and final result"""
        
        # Parse the command - first word is tool name, rest is args
        parts = prompt.strip().split(maxsplit=1)
        tool_name = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        # Yield thinking state
        yield {"type": "thinking", "turn": 1}
        
        # Check if tool exists
        if tool_name in self.tools:
            # Execute the tool
            result = await self.tools[tool_name](args)
            yield {"type": "result", "content": result}
        else:
            yield {"type": "result", "content": f"Unknown command: {tool_name}"}
        
        # Done
        yield {"type": "terminal", "state": TerminalState.COMPLETED}
