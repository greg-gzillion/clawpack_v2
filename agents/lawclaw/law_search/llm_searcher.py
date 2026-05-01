"""LLM-powered law case search

   CONSTITUTIONAL UPDATE: All model access now routes through shared/llm/client.py
   The sovereign gateway. No direct provider access. No invisible legal queries.
   
   Every case law search is now audited, budgeted, and governed.
"""

import sys
from pathlib import Path

_current = Path(__file__).resolve()
_project_root = _current.parent.parent.parent.parent
sys.path.insert(0, str(_project_root))


class LLMLawSearcher:
    def __init__(self):
        self._llm = None          # Sovereign gateway - initialized on first use
        self.chronicle = None
        self._init_chronicle()
    
    @property
    def llm(self):
        """THE SOVEREIGN GATEWAY — All model access passes through here.
        
        No agent may speak to a model directly.
        Every legal query is audited, budgeted, and governed.
        """
        if self._llm is None:
            from shared.llm import get_llm_client
            self._llm = get_llm_client()
        return self._llm
    
    def _init_chronicle(self):
        try:
            from shared.chronicle_helper import search_chronicle
            self.chronicle = search_chronicle
            print("✅ Chronicle connected", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ Chronicle error: {e}", file=sys.stderr)
    
    def search_case_law(self, query: str) -> str:
        """Use governed LLM access to search and analyze case law.
        
        Every query is:
        - Routed through the sovereign gateway
        - Logged to Chronicle with full audit metadata
        - Subject to budget enforcement
        - Controlled by llmclaw /use for model selection
        """
        
        try:
            available = self.llm.list_models()
        except Exception:
            available = []
        
        if not available:
            return (
                f"⚠️ Sovereign gateway reports no models available.\n\n"
                f"Try: https://scholar.google.com/scholar?q={query.replace(' ', '+')}"
            )
        
        prompt = f"""You are a legal research assistant. Analyze case law about: {query}

Provide:
1. Key Supreme Court cases related to {query}
2. Brief summary of each case
3. The ruling and significance
4. Year and citation if known

Be concise and accurate."""
        
        try:
            response = self.llm.call_sync(
                prompt=prompt,
                agent="lawclaw",
                capability="legal_research",
            )
            return (
                f"⚖️ CASE LAW: {query}\n"
                f"   Model: {response.model} | Provider: {response.provider.value}\n"
                f"   Tokens: {response.tokens_used} | Cost: ${response.cost:.6f}\n"
                f"   Audit: {response.request_hash}\n\n"
                f"{response.content}"
            )
        except Exception as e:
            raise RuntimeError(
                f"SOVEREIGN GATEWAY FAILURE in lawclaw/llm_searcher: "
                f"The throne is unreachable. No legal research is possible "
                f"without constitutional authority. Underlying error: {e}"
            ) from e


llm_searcher = LLMLawSearcher()