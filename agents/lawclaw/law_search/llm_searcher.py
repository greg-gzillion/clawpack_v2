"""LLM-powered law case search"""

import sys
from pathlib import Path

# Find the actual project root (clawpack_v2)
_current = Path(__file__).resolve()
_project_root = _current.parent.parent.parent.parent  # agents/lawclaw/law_search -> clawpack_v2
sys.path.insert(0, str(_project_root))

class LLMLawSearcher:
    def __init__(self):
        self.llm = None
        self.chronicle = None
        self._init_llm()
        self._init_chronicle()
    
    def _init_llm(self):
        try:
            from core.llm_manager import get_llm_manager
            self.llm = get_llm_manager()
            if self.llm and hasattr(self.llm, 'groq_client') and self.llm.groq_client:
                print("✅ LLM (Groq) connected", file=sys.stderr)
            else:
                print("⚠️ LLM not available", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ LLM error: {e}", file=sys.stderr)
    
    def _init_chronicle(self):
        try:
            from shared.chronicle_helper import search_chronicle
            self.chronicle = search_chronicle
            print("✅ Chronicle connected", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ Chronicle error: {e}", file=sys.stderr)
    
    def search_case_law(self, query: str) -> str:
        """Use LLM to search and analyze case law"""
        
        if not self.llm:
            return f"⚠️ LLM not available. Please check GROQ_API_KEY in .env\n\nTry: https://scholar.google.com/scholar?q={query.replace(' ', '+')}"
        
        prompt = f"""You are a legal research assistant. Analyze case law about: {query}

Provide:
1. Key Supreme Court cases related to {query}
2. Brief summary of each case
3. The ruling and significance
4. Year and citation if known

Be concise and accurate."""
        
        try:
            response = self.llm.chat_sync(prompt, task_type="legal")
            return f"⚖️ CASE LAW: {query}\n\n{response}"
        except Exception as e:
            return f"LLM error: {e}"

llm_searcher = LLMLawSearcher()
