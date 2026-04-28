#!/usr/bin/env python3
"""Chronicle bridge for CrustyClaw - connects to WebClaw and DataClaw"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class ChronicleBridge:
    def __init__(self):
        self.webclaw = None
        self.dataclaw = None
        self._init_connections()
    
    def _init_connections(self):
        try:
            from agents.webclaw.core.chronicle_ledger import get_chronicle
            self.webclaw = get_chronicle()
            print("? Connected to WebClaw Chronicle", file=sys.stderr)
        except Exception as e:
            print(f"?? WebClaw not available: {e}", file=sys.stderr)
        
        try:
            from agents.dataclaw.modules.indexer.local_indexer import LocalIndexer
            self.dataclaw = LocalIndexer()
            print("? Connected to DataClaw", file=sys.stderr)
        except Exception as e:
            print(f"?? DataClaw not available: {e}", file=sys.stderr)
    
    def search(self, query, source="both", limit=2000000):
        results = []
        if source in ["webclaw", "both"] and self.webclaw:
            try:
                from shared.chronicle_helper import search_chronicle
                web_results = search_chronicle(query, limit)
                for r in web_results:
                    results.append({
                        'url': getattr(r, 'url', str(r)),
                        'source': 'webclaw',
                        'context': getattr(r, 'context', '')
                    })
            except:
                pass
        
        if source in ["dataclaw", "both"] and self.dataclaw:
            try:
                data_results = self.dataclaw.search_local(query, limit)
                for r in data_results:
                    results.append({
                        'url': r.get('url', ''),
                        'source': 'dataclaw',
                        'context': r.get('context', '')
                    })
            except:
                pass
        
        return results
    
    def stats(self):
        stats = {'webclaw': {}, 'dataclaw': {}}
        if self.webclaw:
            try:
                w_stats = self.webclaw.get_stats()
                stats['webclaw'] = {
                    'total_cards': w_stats.get('total_cards', 0),
                    'unique_urls': w_stats.get('unique_urls', 0)
                }
            except:
                pass
        return stats

if __name__ == "__main__":
    bridge = ChronicleBridge()
    print("\n=== CRUSTYCLAW CHRONICLE BRIDGE ===")
    print(f"Stats: {bridge.stats()}")
    
    results = bridge.search("rust code", "both", 5)
    print(f"\nSearch results: {len(results)} found")
    for r in results:
        print(f"   {r['url']}... ({r['source']})")
