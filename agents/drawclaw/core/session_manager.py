"""Session Manager - Tracks drawings and statistics"""

from datetime import datetime
from typing import List, Dict

class SessionManager:
    def __init__(self):
        self.queries: List[Dict] = []
        self.drawings: List[Dict] = []
    
    def add_query(self, operation: str, input_data: str):
        self.queries.append({
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "input": input_data
        })
    
    def add_drawing(self, name: str, filepath: str):
        self.drawings.append({
            "name": name,
            "filepath": filepath,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_drawings(self) -> List[Dict]:
        return self.drawings[-20:]  # Last 20 drawings
    
    def get_stats(self) -> Dict:
        operations = {}
        for q in self.queries:
            op = q["operation"]
            operations[op] = operations.get(op, 0) + 1
        
        return {
            "total_queries": len(self.queries),
            "total_drawings": len(self.drawings),
            "operations": operations,
            "recent_drawings": self.drawings[-5:] if self.drawings else []
        }
