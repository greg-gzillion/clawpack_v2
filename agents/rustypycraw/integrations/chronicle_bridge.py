"""Bridge to connect rustypycraw with webclaw and dataclaw chronicle indexes"""

import sys
from pathlib import Path
from typing import List, Dict, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class ChronicleBridge:
    """Bridge between rustypycraw and chronicle indexes (webclaw + dataclaw)"""
    
    def __init__(self):
        self.webclaw_chronicle = None
        self.dataclaw_index = None
        self._init_connections()
    
    def _init_connections(self):
        """Initialize connections to chronicle systems"""
        try:
            from agents.webclaw.core.chronicle_ledger import get_chronicle
            self.webclaw_chronicle = get_chronicle()
            print("✅ Connected to WebClaw Chronicle", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ WebClaw Chronicle not available: {e}", file=sys.stderr)
        
        try:
            from agents.dataclaw.modules.indexer.local_indexer import LocalIndexer
            self.dataclaw_index = LocalIndexer()
            print("✅ Connected to DataClaw Index", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ DataClaw Index not available: {e}", file=sys.stderr)
    
    def search_webclaw(self, query: str, limit: int = 10) -> List[Dict]:
        """Search webclaw chronicle for code references"""
        if not self.webclaw_chronicle:
            return []
        
        try:
            from shared.chronicle_helper import search_chronicle
            results = search_chronicle(f"rustypycraw {query}", limit)
            return [
                {
                    'url': getattr(r, 'url', str(r)),
                    'context': getattr(r, 'context', ''),
                    'source': getattr(r, 'source', 'webclaw')
                }
                for r in results
            ]
        except Exception as e:
            print(f"WebClaw search error: {e}", file=sys.stderr)
            return []
    
    def search_dataclaw(self, query: str, limit: int = 10) -> List[Dict]:
        """Search dataclaw local index for code references"""
        if not self.dataclaw_index:
            return []
        
        try:
            results = self.dataclaw_index.search_local(query, limit)
            return results
        except Exception as e:
            print(f"DataClaw search error: {e}", file=sys.stderr)
            return []
    
    def unified_search(self, query: str, limit: int = 10) -> Dict:
        """Search both indexes and combine results"""
        webclaw_results = self.search_webclaw(query, limit)
        dataclaw_results = self.search_dataclaw(query, limit)
        
        return {
            'query': query,
            'webclaw': webclaw_results,
            'dataclaw': dataclaw_results,
            'total': len(webclaw_results) + len(dataclaw_results)
        }
    
    def index_code_to_chronicle(self, file_path: str, content: str, language: str) -> bool:
        """Index code directly to chronicle"""
        if not self.webclaw_chronicle:
            return False
        
        try:
            self.webclaw_chronicle.record_fetch(
                url=f"file://{file_path}",
                context=f"Code: {Path(file_path).name}\n{content}",
                source=f"rustypycraw/{language}",
                metadata={
                    'language': language,
                    'path': file_path,
                    'analyzed': True
                }
            )
            return True
        except Exception as e:
            print(f"Index error: {e}", file=sys.stderr)
            return False
    
    def get_code_context(self, code_snippet: str) -> List[Dict]:
        """Get relevant context from chronicle for code analysis"""
        # Search for similar code patterns
        webclaw_results = self.search_webclaw(code_snippet, 5)
        dataclaw_results = self.search_dataclaw(code_snippet, 5)
        
        return webclaw_results + dataclaw_results
    
    def sync_dataclaw_references(self) -> str:
        """Sync all dataclaw references to rustypycraw context"""
        if not self.dataclaw_index:
            return "DataClaw not available"
        
        try:
            # Search for code-related documents in dataclaw
            results = self.dataclaw_index.search_local("code", 20)
            return f"✅ Synced {len(results)} references from DataClaw"
        except Exception as e:
            return f"Sync error: {e}"
    
    def get_chronicle_stats(self) -> Dict:
        """Get statistics from both chronicle systems"""
        stats = {'webclaw': {}, 'dataclaw': {}}
        
        if self.webclaw_chronicle:
            try:
                w_stats = self.webclaw_chronicle.get_stats()
                stats['webclaw'] = {
                    'total_cards': w_stats.get('total_cards', 0),
                    'unique_urls': w_stats.get('unique_urls', 0)
                }
            except:
                pass
        
        if self.dataclaw_index and hasattr(self.dataclaw_index, 'chronicle'):
            try:
                d_stats = self.dataclaw_index.chronicle.get_stats()
                stats['dataclaw'] = {
                    'total_cards': d_stats.get('total_cards', 0),
                    'unique_urls': d_stats.get('unique_urls', 0)
                }
            except:
                pass
        
        return stats

# Global bridge instance
chronicle_bridge = ChronicleBridge()
