"""Chronicle References Module - Enhanced Search"""

import sys
from pathlib import Path

CLAWPACK_ROOT = Path("/home/greg/dev/clawpack_v2")
sys.path.insert(0, str(CLAWPACK_ROOT))

class ReferenceHandler:
    def __init__(self, ai_assistant=None):
        self.ai = ai_assistant
        self.chronicle = None
        self._init_chronicle()
    
    def _init_chronicle(self):
        try:
            from shared.chronicle_helper import search_chronicle
            self.chronicle = search_chronicle
            print("✅ Chronicle handler ready", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ Chronicle error: {e}", file=sys.stderr)
    
    def search(self, query, max_results=5):
        """Search chronicle for TX.org references - case insensitive"""
        if not self.chronicle:
            return []
        
        # Try multiple search variations
        search_variations = [
            query,
            query.lower(),
            query.upper(),
            f"*{query}*",
            query.replace(' ', '*'),
        ]
        
        all_results = []
        seen = set()
        
        for term in search_variations[:3]:
            try:
                results = self.chronicle(term, max_results)
                for r in results:
                    url = getattr(r, 'url', str(r))
                    if url not in seen:
                        seen.add(url)
                        all_results.append({
                            'url': url,
                            'source': getattr(r, 'source', 'chronicle'),
                            'term': term
                        })
            except:
                pass
        
        # Also try direct search for common patterns
        common_patterns = [
            f"cosmwasm {query}",
            f"tx.org {query}",
            f"rust {query}",
            f"auction {query}"
        ]
        
        for pattern in common_patterns[:2]:
            try:
                results = self.chronicle(pattern, 2)
                for r in results:
                    url = getattr(r, 'url', str(r))
                    if url not in seen:
                        seen.add(url)
                        all_results.append({
                            'url': url,
                            'source': getattr(r, 'source', 'chronicle'),
                            'term': pattern
                        })
            except:
                pass
        
        return all_results[:max_results]
    
    def get_docs(self, topic):
        """Get documentation links for a topic"""
        results = self.search(topic, 5)
        return [r['url'] for r in results]
    
    def format_references(self, references):
        """Format references for display"""
        if not references:
            return "No references found in chronicle. Try 'cosmwasm', 'tx.org', or 'rust'"
        
        output = "📚 References from Chronicle Index:\n"
        for i, ref in enumerate(references[:5], 1):
            output += f"{i}. {ref['url']}\n"
            if ref.get('source'):
                output += f"   (from: {ref['source']})\n"
        return output
