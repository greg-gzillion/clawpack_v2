"""Command Router - Routes commands to appropriate agents"""
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple

class CommandRouter:
    def __init__(self, loaded_agents: dict):
        self.agents = loaded_agents
        self.agents_path = Path("agents")
        self.route_map = self._build_route_map()
    
    def _build_route_map(self) -> dict:
        route_map = {
            "translate": "interpretclaw",
            "speak": "interpretclaw",`n            "listen": "interpretclaw",
            "solve": "mathematicaclaw",
            "plot": "plotclaw",
            "dream": "dreamclaw",
            "search": "webclaw",
            "fetch": "webclaw",
            "stats": "dataclaw",
            "analyze": "dataclaw",
            "legal": "lawclaw",
            "medical": "mediclaw",
        }
        for agent_name, agent_data in self.agents.items():
            for cmd in agent_data.get("commands", []):
                if cmd not in route_map:
                    route_map[cmd] = agent_name
        return route_map
    
    def list_agents(self) -> str:
        """List all loaded agents"""
        output = ["\n📦 Loaded Agents:\n"]
        for name, data in self.agents.items():
            cmd_count = len(data.get("commands", []))
            output.append(f"  • {name} ({cmd_count} commands)")
        return '\n'.join(output)
    
    def help(self) -> str:
        """Show help"""
        return """
🦞 CLAWPACK COMMANDS:

  /llms              - List all 23 LLMs
  /use <model>       - Select specific model
  /use liberated     - Use liberated models
  /model             - Show current model
  /agents            - List all agents
  /help              - Show this help
  /quit              - Exit

  Agent Commands:
    translate <text> to <lang>
    speak <text>
    solve <equation>
    plot <expression>
    dream <prompt>
    search <query>
    fetch <url>
    /stats
"""
    
    def route(self, user_input: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        cmd_parts = user_input.strip().split(maxsplit=1)
        if not cmd_parts:
            return None, None, None
        
        command = cmd_parts[0].lower()
        args = cmd_parts[1] if len(cmd_parts) > 1 else ""
        
        if command in self.route_map:
            return self.route_map[command], command, args
        
        user_lower = user_input.lower()
        if " to " in user_lower:
            return "interpretclaw", "translate", user_input
        
        return None, None, None
    
    def execute(self, agent_name: str, command: str, args: str) -> str:
        agent_path = self.agents_path / agent_name / f"{agent_name}.py"
        if not agent_path.exists():
            return f"Agent not found: {agent_name}"
        
        full_cmd = f"{command} {args}".strip() if command else args
        
        try:
            result = subprocess.run(
                [sys.executable, str(agent_path), full_cmd],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.agents_path.parent)
            )
            return result.stdout.strip() or result.stderr.strip() or "Done"
        except subprocess.TimeoutExpired:
            return "Command timed out"
        except Exception as e:
            return f"Error: {e}"

