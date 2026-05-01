"""
CONSTITUTIONAL UPDATE: WebClaw API now routes through sovereign gateway.

This was a shared utility that taught multiple agents how to bypass governance.
Now it's an adapter that demonstrates constitutional compliance.
All model access passes through shared/llm/client.py with full audit trail.
"""

import sys
import warnings
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

warnings.warn(
    "webclaw/core/api.py is DEPRECATED as an independent authority. "
    "All LLM calls now route through shared/llm/client.py. "
    "This adapter will be removed once all agents use shared/llm directly.",
    DeprecationWarning,
    stacklevel=2
)

__all__ = ["WebAPI", "get_web_api"]  # Predictable transition


class WebAPI:
    """ADAPTER ONLY — Delegates all LLM calls to the sovereign gateway.
    
    This is NOT an independent API. It has no model access authority.
    All web search enrichment, content analysis, and LLM operations
    now route through shared/llm/client.py for:
    - Audit logging (Chronicle)
    - Budget enforcement
    - Model governance (respects llmclaw /use)
    - Provider fallback
    """
    
    def __init__(self):
        self._client = None
        print("✅ WebAPI initialized — routing through sovereign gateway")
    
    @property
    def client(self):
        """THE SOVEREIGN GATEWAY — All model access passes through here."""
        if self._client is None:
            from shared.llm import get_llm_client
            self._client = get_llm_client()
        return self._client
    
    def ask_llm(self, prompt: str, task_type: str = "web_search") -> dict:
        """Route web search queries through sovereign gateway.
        
        Args:
            prompt: The search/analysis prompt
            task_type: Type of web operation for audit trail
            
        Returns:
            Dict with full audit metadata
        """
        try:
            response = self.client.call_sync(
                prompt=prompt,
                agent="webclaw",
                capability=task_type,
            )
            return {
                'content': response.content,
                'model': response.model,
                'provider': response.provider.value,
                'tokens': response.tokens_used,
                'cost': response.cost,
                'audit_hash': response.request_hash,
                'timestamp': response.timestamp,
            }
        except Exception as e:
            raise RuntimeError(
                f"SOVEREIGN GATEWAY FAILURE in webclaw/core/api.py: "
                f"The throne is unreachable. Web search cannot proceed "
                f"without constitutional authority. Underlying error: {e}"
            ) from e
    
    def enrich_search_results(self, results: list, query: str) -> list:
        """Enrich search results with LLM analysis through sovereign gateway.
        
        This was a silent cost sink. Now every enrichment is audited and budgeted.
        """
        if not results:
            return results
        
        enriched = []
        for result in results:
            prompt = f"Analyze this search result for query '{query}': {result.get('title', '')} - {result.get('snippet', '')}"
            analysis = self.ask_llm(prompt, task_type="search_enrichment")
            
            enriched.append({
                **result,
                'analysis': analysis['content'],
                'audit_hash': analysis['audit_hash'],
                'model': analysis['model'],
                'cost': analysis['cost'],
            })
        
        return enriched
    
    def is_available(self) -> bool:
        """Check if sovereign gateway is accessible."""
        try:
            return len(self.client.list_models()) > 0
        except Exception:
            return False
    
    def get_usage_stats(self) -> dict:
        """Get webclaw-specific usage statistics from Chronicle."""
        try:
            stats = self.client.get_stats()
            return {
                'total_searches': stats.get('by_agent', {}).get('webclaw', 0),
                'total_cost': stats.get('total_cost', 0.0),
                'sovereign_gateway': True,
            }
        except Exception:
            return {
                'total_searches': 0,
                'total_cost': 0.0,
                'sovereign_gateway': False,
                'error': 'Chronicle unreachable'
            }


# Global instance preserved for backward compatibility
_web_api = None

def get_web_api() -> WebAPI:
    """Factory function — preserved for backward compatibility."""
    global _web_api
    if _web_api is None:
        _web_api = WebAPI()
    return _web_api