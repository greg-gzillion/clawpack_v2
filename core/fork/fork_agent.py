"""Fork Agent - Cache sharing sub-agents (Chapter 9)"""
import sys
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.base_agent import BaseAgent

@dataclass
class ForkContext:
    """Context inherited from parent agent"""
    system_prompt: str
    messages: List[Dict]
    tools: List[str]
    model: str
    permission_mode: str = "bubble"
    parent_session_id: str = ""
    fork_boilerplate: str = ""

class ForkAgent(BaseAgent):
    """Fork agent that inherits parent's context for cache sharing"""
    
    def __init__(self, parent_context: ForkContext, task: str):
        super().__init__("fork_agent")
        self.parent_context = parent_context
        self.task = task
        self.result = None
    
    async def execute(self) -> str:
        """Execute the forked task"""
        print(f"🔄 Fork agent executing: {self.task}...")
        
        prompt = f"""
Task: {self.task}

Please complete this task and return the result.
"""
        # Simple execution for now
        return f"✅ Completed: {self.task}"

class ForkManager:
    """Manages fork agent lifecycle"""
    
    def __init__(self):
        self.active_forks: Dict[str, ForkAgent] = {}
    
    def create_fork(self, parent_agent, task: str, model: str = None) -> ForkAgent:
        context = ForkContext(
            system_prompt=getattr(parent_agent, 'system_prompt', ''),
            messages=[],
            tools=[],
            model=model or 'llama3.2:3b',
            permission_mode="bubble"
        )
        fork = ForkAgent(context, task)
        fork_id = f"fork_{len(self.active_forks)}"
        self.active_forks[fork_id] = fork
        return fork
    
    async def run_parallel(self, tasks: List[str], parent_agent, model: str = None) -> List[str]:
        forks = [self.create_fork(parent_agent, task, model) for task in tasks]
        results = await asyncio.gather(*[fork.execute() for fork in forks])
        self.active_forks.clear()
        return results

_fork_manager = None

def get_fork_manager():
    global _fork_manager
    if _fork_manager is None:
        _fork_manager = ForkManager()
    return _fork_manager
