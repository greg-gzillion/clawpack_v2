"""Index local files into chronicle"""

import sys
from pathlib import Path

CLAWPACK_ROOT = Path("/home/greg/dev/clawpack_v2")
sys.path.insert(0, str(CLAWPACK_ROOT))

class LocalIndexer:
    def __init__(self):
        self.chronicle = None
        self._init_chronicle()
    
    def _init_chronicle(self):
        try:
            from agents.webclaw.core.chronicle_ledger import get_chronicle
            self.chronicle = get_chronicle()
            print("✅ Chronicle connected for local indexing", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ Chronicle error: {e}", file=sys.stderr)
    
    def index_file(self, file_info: dict, metadata: dict = None) -> bool:
        """Index a local file in chronicle"""
        if not self.chronicle:
            return False
        
        context = f"Local {file_info['type']}: {file_info['name']}"
        if metadata:
            context += f" - {metadata.get('title', file_info['name'])}"
        
        try:
            self.chronicle.record_fetch(
                url=f"file://{file_info['path']}",
                context=context,
                source=f"dataclaw/{file_info['type']}",
                metadata={
                    'name': file_info['name'],
                    'size_mb': file_info['size_mb'],
                    'type': file_info['type'],
                    'modified': file_info['modified']
                }
            )
            return True
        except:
            return False
    
    def search_local(self, query: str, max_results=10) -> list:
        """Search indexed local files"""
        if not self.chronicle:
            return []
        
        try:
            from shared.chronicle_helper import search_chronicle
            results = search_chronicle(f"dataclaw {query}", max_results)
            return [{'url': getattr(r, 'url', str(r)), 'context': getattr(r, 'context', '')} for r in results]
        except:
            return []
