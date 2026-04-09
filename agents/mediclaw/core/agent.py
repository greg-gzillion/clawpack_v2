"""Mediclaw Agent - Standalone"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

class MediclawAgent:
    def __init__(self):
        self.session = {"queries": []}
    
    def search(self, query: str):
        return {"query": query, "results": []}
    
    def get_stats(self):
        return {"queries": len(self.session["queries"])}
