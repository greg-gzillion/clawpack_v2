"""Modular Agent Loader - Handles relative imports properly"""
import importlib.util
import sys
from pathlib import Path
from typing import Dict, Any, Optional

class AgentLoader:
    def __init__(self):
        self.agents_dir = Path(__file__).parent.parent / "agents"
        self.loaded_agents: Dict[str, Any] = {}
    
    async def load_all(self) -> Dict[str, Any]:
        """Load all agents asynchronously"""
        agents = {}
        
        for agent_path in self.agents_dir.iterdir():
            if not agent_path.is_dir():
                continue
            if agent_path.name.startswith(('_', '__')):
                continue
            
            # Look for agent.py or {name}.py
            agent_file = agent_path / "agent.py"
            if not agent_file.exists():
                agent_file = agent_path / f"{agent_path.name}.py"
            if not agent_file.exists():
                continue
            
            # Load the agent
            agent = await self._load_agent(agent_path.name, agent_file)
            agents[agent_path.name] = agent
            
            if agent:
                print(f"  ✅ {agent_path.name}")
            else:
                print(f"  ⚠️ {agent_path.name} (failed)")
        
        return agents
    
    async def _load_agent(self, name: str, path: Path) -> Optional[Any]:
        """Load a single agent with proper path setup"""
        try:
            # Add parent directory to path for shared imports
            parent_dir = str(path.parent.parent.parent)
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)
            
            # Also add the agent's own directory
            agent_dir = str(path.parent)
            if agent_dir not in sys.path:
                sys.path.insert(0, agent_dir)
            
            # Import the module
            spec = importlib.util.spec_from_file_location(name, path)
            if spec is None:
                return None
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find the agent class (should be {Name}Agent or {name}Agent)
            for attr in dir(module):
                if attr.endswith('Agent') and attr != 'BaseAgent':
                    agent_class = getattr(module, attr)
                    return agent_class()
            
            # If no class found, return the module itself
            return module
            
        except Exception as e:
            print(f"  ⚠️ Failed to load {name}: {e}")
            return None
