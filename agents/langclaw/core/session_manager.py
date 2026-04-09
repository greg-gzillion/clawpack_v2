"""Session Manager - Tracks translation history and statistics"""

from typing import List, Dict
from datetime import datetime

class SessionManager:
    def __init__(self):
        self.queries: List[Dict] = []
    
    def add_query(self, text: str, target_lang: str, success: bool, translation: str = None):
        self.queries.append({
            "timestamp": datetime.now().isoformat(),
            "text": text,
            "target": target_lang,
            "success": success,
            "translation": translation
        })
    
    def get_stats(self) -> Dict:
        total = len(self.queries)
        successful = sum(1 for q in self.queries if q["success"])
        return {
            "total_queries": total,
            "successful": successful,
            "failed": total - successful,
            "queries": self.queries
        }
    
    def get_recent(self, limit: int = 5) -> List[Dict]:
        return self.queries[-limit:] if self.queries else []
