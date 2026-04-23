"""DataClaw Integration Hub - Connects to all clawpack agents"""

import sys
from pathlib import Path

CLAWPACK_ROOT = Path("/home/greg/dev/clawpack_v2")
sys.path.insert(0, str(CLAWPACK_ROOT))

class AgentHub:
    """Central hub connecting DataClaw to all agents"""
    
    def __init__(self):
        self.agents = {}
        self._load_agents()
    
    def _load_agents(self):
        """Load all available agents"""
        agent_map = {
            'webclaw': 'agents/webclaw/webclaw.py',
            'flowclaw': 'agents/flowclaw/flowclaw.py',
            'docuclaw': 'agents/docuclaw/docuclaw.py',
            'mathematicaclaw': 'agents/mathematicaclaw/mathematicaclaw.py',
            'txclaw': 'agents/txclaw/txclaw.py',
            'lawclaw': 'agents/lawclaw/lawclaw.py',
            'langclaw': 'agents/langclaw/langclaw.py',
            'mediclaw': 'agents/mediclaw/mediclaw.py'
        }
        
        for name, path in agent_map.items():
            full_path = CLAWPACK_ROOT / path
            if full_path.exists():
                self.agents[name] = {'path': str(full_path), 'loaded': False}
    
    def get_agent_list(self):
        return list(self.agents.keys())
    
    def sync_to_webclaw(self, file_info):
        """Sync local file reference to webclaw's chronicle"""
        try:
            from shared.chronicle_helper import search_chronicle
            # Record the local file in chronicle
            search_chronicle(f"file://{file_info['path']}", 1)
            return True
        except:
            return False
    
    def provide_context_to_agent(self, agent_name, query):
        """Provide local reference context to a specific agent"""
        from modules.search.local_search import LocalSearch
        searcher = LocalSearch()
        
        # Search local files for relevant content
        results = searcher.search_files(query, None)
        
        if not results:
            return None
        
        context = f"\n[DataClaw] Local references found for '{query}':\n"
        for r in results:
            context += f"  • {r['name']} ({r['size_mb']} MB) - {r['path']}\n"
        
        return context
    
    def get_local_references_for_prompt(self, query, agent_name):
        """Get formatted local references for agent prompts"""
        from modules.search.local_search import LocalSearch
        searcher = LocalSearch()
        
        results = searcher.search_files(query, None)
        
        if not results:
            return ""
        
        ref_text = f"\n\n## Local References (from DataClaw) for {agent_name}:\n"
        for r in results:
            ref_text += f"- {r['name']} (local file)\n"
        
        return ref_text

# Global instance
agent_hub = AgentHub()
