"""TXClaw AI Assistant - Connected to Chronicle Index"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class TXAIAssistant:
    def __init__(self):
        self.llm = None
        self.chronicle = None
        self._init_llm()
        self._init_chronicle()
    
    def _init_llm(self):
        try:
            from core.llm_manager import get_llm_manager
            self.llm = get_llm_manager()
            if self.llm:
                print("✅ TX AI: LLM Connected", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ TX AI: LLM error: {e}", file=sys.stderr)
    
    def _init_chronicle(self):
        try:
            from shared.chronicle_helper import search_chronicle
            self.chronicle = search_chronicle
            print("✅ TX AI: Chronicle Connected", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ TX AI: Chronicle error: {e}", file=sys.stderr)
    
    def search(self, query, max_results=5):
        """Search chronicle for TX.org/CosmWasm resources"""
        if not self.chronicle:
            return []
        
        search_terms = [
            f"tx.org {query}",
            f"cosmwasm {query}",
            f"TX.org {query}",
            f"blockchain {query}"
        ]
        
        results = []
        seen = set()
        
        for term in search_terms[:3]:
            try:
                refs = self.chronicle(term, 2)
                for r in refs:
                    url = getattr(r, 'url', str(r))
                    if url not in seen:
                        seen.add(url)
                        results.append({'url': url, 'source': term})
            except:
                pass
        
        return results[:max_results]
    
    def generate_code(self, prompt, context=None):
        """Generate code using LLM with chronicle context"""
        if not self.llm:
            return None
        
        full_prompt = prompt
        if context:
            full_prompt = f"{context}\n\n{prompt}"
        
        try:
            return self.llm.chat_sync(full_prompt, task_type="coding")
        except:
            return None
    
    def is_available(self):
        return self.llm is not None
