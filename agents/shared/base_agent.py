"""Base agent class for all clawpack agents"""

import json
from pathlib import Path
from datetime import datetime

class BaseAgent:
    def __init__(self, name: str):
        self.name = name
        self.interactions = 0
        self.memory_path = Path.home() / ".clawpack" / "memory" / name
        self.memory_path.mkdir(parents=True, exist_ok=True)
        self._load_state()
    
    def _load_state(self):
        state_file = self.memory_path / "state.json"
        if state_file.exists():
            try:
                data = json.loads(state_file.read_text())
                self.interactions = data.get('interactions', 0)
            except:
                pass
    
    def _save_state(self):
        state_file = self.memory_path / "state.json"
        state_file.write_text(json.dumps({
            'interactions': self.interactions,
            'last_active': datetime.now().isoformat()
        }, indent=2))
    
    def track_interaction(self):
        self.interactions += 1
        self._save_state()
    
    def handle(self, query: str) -> str:
        """Handle a query - to be overridden by subclasses"""
        raise NotImplementedError
    
    def get_stats(self) -> dict:
        return {
            'name': self.name,
            'interactions': self.interactions,
            'memory_path': str(self.memory_path)
        }
