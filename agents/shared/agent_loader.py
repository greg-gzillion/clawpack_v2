"""Agent loader with graceful fallbacks"""

import sys
from pathlib import Path

def load_agent(agent_name: str, agent_path: Path):
    """Load an agent with graceful fallback"""
    try:
        # Add agent directory to path
        sys.path.insert(0, str(agent_path))
        
        # Try to import the agent
        spec = __import__(f"{agent_name}")
        
        # Look for agent class
        for attr_name in dir(spec):
            if attr_name.lower() == f"{agent_name}agent" or attr_name.endswith("Agent"):
                agent_class = getattr(spec, attr_name)
                return agent_class()
        
        # Fallback: create a simple agent
        return SimpleAgent(agent_name)
    except Exception as e:
        print(f"  ⚠️ {agent_name}: {e}", file=sys.stderr)
        return SimpleAgent(agent_name)

class SimpleAgent:
    """Fallback agent when full implementation isn't available"""
    def __init__(self, name):
        self.name = name
        self.description = f"{name} agent (basic mode)"
    
    def handle(self, query):
        return f"{self.name}: Processing '{query}' (basic mode)"
    
    def process(self, cmd, *args):
        return self.handle(' '.join(args))

def get_available_agents():
    """Return list of all agent directories"""
    agents_dir = Path(__file__).parent.parent
    agents = []
    for agent_dir in agents_dir.iterdir():
        if agent_dir.is_dir() and not agent_dir.name.startswith('_'):
            if agent_dir.name.endswith('claw') or agent_dir.name in ['shared', 'crustyclaw', 'rustypycraw']:
                agents.append(agent_dir.name)
    return agents
