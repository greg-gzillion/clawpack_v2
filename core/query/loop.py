"""The Query Loop - Heartbeat of Clawpack"""
import asyncio
import subprocess
import sys
from pathlib import Path
from typing import AsyncGenerator, List, Dict, Any

class QueryConfig:
    def __init__(self, max_turns=10, auto_compact=True, permission_mode="default"):
        self.max_turns = max_turns
        self.auto_compact = auto_compact
        self.permission_mode = permission_mode

class QueryLoop:
    def __init__(self, config: QueryConfig, context: Dict[str, Any]):
        self.config = config
        self.context = context
        self.agents_path = Path("agents")
    
    async def query(self, messages: List[Dict]) -> AsyncGenerator[Dict, None]:
        """Execute the agent loop"""
        if not messages:
            yield {"role": "assistant", "content": "No messages"}
            return
        
        last_msg = messages[-1]
        user_input = last_msg.get("content", "").strip()
        
        # Route to appropriate agent
        agent_name, command = self._route_command(user_input)
        
        if agent_name:
            result = await self._execute_agent(agent_name, command)
            yield {"role": "assistant", "content": result}
        else:
            yield {"role": "assistant", "content": f"Unknown command: {user_input}"}
    
    def _route_command(self, user_input: str) -> tuple:
        """Route command to appropriate agent - returns (agent_name, command)"""
        cmd_lower = user_input.lower()
        
        # Translation
        if cmd_lower.startswith("translate"):
            return "interpretclaw", user_input
        
        # Speak
        elif cmd_lower.startswith("speak"):
            return "interpretclaw", user_input
        
        # Math
        elif cmd_lower.startswith("solve"):
            return "mathematicaclaw", user_input
        
        # Plot
        elif cmd_lower.startswith("plot"):
            return "plotclaw", user_input
        
        # Dream
        elif cmd_lower.startswith("dream"):
            return "dreamclaw", user_input
        
        # Search
        elif cmd_lower.startswith("search"):
            return "webclaw", user_input
        
        # Court
        elif "/court" in cmd_lower:
            return "lawclaw", user_input
        
        # Stats/Data
        elif "/stats" in cmd_lower or cmd_lower.startswith("analyze"):
            return "dataclaw", user_input
        
        # Documents
        elif "/list" in cmd_lower:
            return "docuclaw", user_input
        
        # Flowchart
        elif "flowchart" in cmd_lower:
            return "flowclaw", user_input
        
        # Default - try webclaw
        else:
            return "webclaw", f"search {user_input}"
    
    async def _execute_agent(self, agent_name: str, command: str) -> str:
        """Execute an agent with the given command"""
        agent_path = self.agents_path / agent_name / f"{agent_name}.py"
        
        if not agent_path.exists():
            return f"Agent not found: {agent_name}"
        
        try:
            # Run agent as subprocess
            result = subprocess.run(
                [sys.executable, str(agent_path), command],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(Path.cwd())
            )
            
            output = result.stdout.strip()
            if not output:
                output = result.stderr.strip()
            
            # Clean up output
            lines = []
            for line in output.split('\n'):
                line = line.strip()
                if line and not line.startswith('===') and not line.startswith('COMMANDS'):
                    if '█' not in line:
                        lines.append(line)
            
            clean_output = '\n'.join(lines).strip()
            
            if clean_output:
                return clean_output
            else:
                return f"[{agent_name}] No output"
                
        except subprocess.TimeoutExpired:
            return f"[{agent_name}] Command timed out"
        except Exception as e:
            return f"[{agent_name}] Error: {e}"

__all__ = ['QueryLoop', 'QueryConfig']
