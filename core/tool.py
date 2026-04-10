"""AgentTool - Wrap agents as unified tools"""
from typing import Dict, Any, Optional
from dataclasses import dataclass
import asyncio
import subprocess
import sys
from pathlib import Path

@dataclass
class ToolResult:
    """Standard tool result"""
    data: Any
    error: Optional[str] = None
    new_messages: Optional[list] = None

class AgentTool:
    """Wrap an agent as a Claude Code-style tool"""
    
    def __init__(self, name: str, agent_data: Dict[str, Any]):
        self.name = name
        self.agent_data = agent_data
        self.agent_path = Path(f"agents/{name}/{name}.py")
        
    @property
    def input_schema(self) -> Dict[str, Any]:
        """JSON Schema for tool input"""
        return {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": f"Command for {self.name}"}
            },
            "required": ["command"]
        }
    
    def is_concurrency_safe(self, input_data: Dict) -> bool:
        """Check if this invocation is safe for parallel execution"""
        # Read-only agents are concurrency-safe
        read_only_agents = {"webclaw", "dataclaw", "mathematicaclaw", "interpretclaw"}
        return self.name in read_only_agents
    
    def is_read_only(self, input_data: Dict) -> bool:
        """Check if this tool only reads data"""
        read_only_agents = {"webclaw", "mathematicaclaw", "interpretclaw"}
        return self.name in read_only_agents
    
    async def call(self, input_data: Dict, context: Dict) -> ToolResult:
        """Execute the agent"""
        command = input_data.get("command", "")
        
        try:
            # Run agent as subprocess (for now - can upgrade to direct import)
            result = subprocess.run(
                [sys.executable, str(self.agent_path), command],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(Path.cwd())
            )
            
            output = result.stdout.strip() or result.stderr.strip()
            
            return ToolResult(
                data={"output": output, "agent": self.name},
                error=None
            )
        except subprocess.TimeoutExpired:
            return ToolResult(
                data=None,
                error=f"Agent {self.name} timed out"
            )
        except Exception as e:
            return ToolResult(
                data=None,
                error=str(e)
            )
