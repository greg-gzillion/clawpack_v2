"""Agent Loader - Discovers and loads all agents"""
import sys
import importlib.util
from pathlib import Path
from typing import Dict, Any, Optional

class AgentLoader:
    def __init__(self):
        self.agents_path = Path("agents")
        self.loaded_agents: Dict[str, Any] = {}
    
    def discover_agents(self) -> list:
        """Find all available agents"""
        agents = []
        for agent_dir in self.agents_path.iterdir():
            if not agent_dir.is_dir():
                continue
            if agent_dir.name.startswith(('_', 'shared', 'langclaw_backup')):
                continue
            
            agent_file = agent_dir / f"{agent_dir.name}.py"
            if agent_file.exists():
                agents.append({
                    "name": agent_dir.name,
                    "path": str(agent_file),
                    "commands": self._discover_commands(agent_dir)
                })
        
        return agents
    
    def _discover_commands(self, agent_dir: Path) -> list:
        """Discover commands an agent supports"""
        commands = []
        commands_dir = agent_dir / "commands"
        if commands_dir.exists():
            for cmd_file in commands_dir.glob("*.py"):
                if not cmd_file.name.startswith("__"):
                    commands.append(cmd_file.stem)
        
        # Also check main file for command patterns
        main_file = agent_dir / f"{agent_dir.name}.py"
        if main_file.exists():
            content = main_file.read_text(encoding='utf-8', errors='ignore')
            if "translate" in content.lower():
                commands.append("translate")
            if "solve" in content.lower():
                commands.append("solve")
            if "plot" in content.lower():
                commands.append("plot")
            if "dream" in content.lower():
                commands.append("dream")
            if "search" in content.lower():
                commands.append("search")
        
        return list(set(commands))
    
    def enable_learning(self, agent):
        agent.learning_enabled = True
    
    def load_agent(self, agent_info: dict) -> Optional[Any]:
        """Load a single agent module"""
        try:
            spec = importlib.util.spec_from_file_location(
                agent_info["name"],
                agent_info["path"]
            )
            module = importlib.util.module_from_spec(spec)
            sys.modules[agent_info["name"]] = module
            spec.loader.exec_module(module)
            
            # Find the agent class
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and attr_name.lower().endswith('claw'):
                    agent_instance = attr()
                    self.loaded_agents[agent_info["name"]] = {
                        "instance": agent_instance,
                        "module": module,
                        "commands": agent_info["commands"]
                    }
                    return agent_instance
            
            # If no class found, use module directly
            self.loaded_agents[agent_info["name"]] = {
                "instance": module,
                "module": module,
                "commands": agent_info["commands"]
            }
            return module
            
        except Exception as e:
            print(f"Error loading {agent_info['name']}: {e}")
            return None
    
    def load_all(self) -> Dict[str, Any]:
        """Load all discovered agents"""
        agents = self.discover_agents()
        print(f"\n📦 Loading {len(agents)} agents...")
        
        for agent_info in agents:
            instance = self.load_agent(agent_info)
            if instance:
                cmd_count = len(agent_info["commands"])
                print(f"  ✅ {agent_info['name']} ({cmd_count} commands)")
        
        return self.loaded_agents

