"""Client for communicating with DataClaw agent"""

from pathlib import Path
from typing import Optional

class DataClawClient:
    """Client to fetch local references from DataClaw"""
    
    def __init__(self):
        self.references_path = Path(__file__).parent.parent.parent / "dataclaw" / "references"
    
    def search(self, category: str, query: str) -> Optional[str]:
        """Search local references"""
        if not self.references_path.exists():
            return None
        
        results = []
        for md_file in self.references_path.rglob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8', errors='ignore')
                if query.lower() in content.lower():
                    results.append(content)
                    if len(results) >= 3:
                        break
            except:
                pass
        
        return "\n\n".join(results) if results else None
