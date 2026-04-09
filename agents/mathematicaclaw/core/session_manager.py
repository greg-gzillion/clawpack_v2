"""Session Manager - Tracks queries and statistics"""

from datetime import datetime
from typing import List, Dict

class SessionManager:
    def __init__(self):
        self.queries: List[Dict] = []
    
    def add_query(self, operation: str, input_data: str):
        self.queries.append({
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "input": input_data
        })
    
    def get_stats(self) -> Dict:
        operations = {}
        for q in self.queries:
            op = q["operation"]
            operations[op] = operations.get(op, 0) + 1
        
        return {
            "total_queries": len(self.queries),
            "operations": operations,
            "recent": self.queries[-5:] if self.queries else []
        }
