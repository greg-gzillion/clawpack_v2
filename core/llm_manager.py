"""ADAPTER — core/llm_manager.py now delegates to the sovereign gateway.

   CONSTITUTIONAL UPDATE: This file was the original intended throne,
   but agents bypassed it. Now it becomes an adapter to the real throne:
   shared/llm/client.py — the single point of model access.

   All calls route through the sovereign gateway for:
   - Audit logging (Chronicle)
   - Budget enforcement
   - Model registry (respects llmclaw /use)
   - Provider fallback
   - Full governance
"""

import warnings

warnings.warn(
    "core/llm_manager.py is DEPRECATED as an authority. "
    "It now delegates to shared/llm/client.py — the sovereign gateway. "
    "Import from shared.llm directly in new code.",
    DeprecationWarning,
    stacklevel=2
)

__all__ = ['get_llm_manager', 'LLMManager']


class LLMManager:
    """ADAPTER ONLY — Delegates all LLM calls to the sovereign gateway.
    
    This is NOT a model manager. It has no independent authority.
    It exists only to prevent breakage during constitutional transition.
    
    All agents that previously imported from core.llm_manager will
    continue to work, but their calls now route through shared/llm/client.py
    with full audit, budget, and governance.
    """
    
    def __init__(self):
        self._client = None
        # groq_client preserved for backward compatibility checks
        # Agents that check 'if self.llm.groq_client' will get a truthy value
        # because the sovereign gateway handles provider selection
        self.groq_client = True  # Sovereign handles provider routing
    
    @property
    def client(self):
        """THE SOVEREIGN GATEWAY — All model access passes through here."""
        if self._client is None:
            from shared.llm import get_llm_client
            self._client = get_llm_client()
        return self._client
    
    @property
    def has_groq(self):
        """Truthful delegation — check sovereign, not local state."""
        try:
            models = self.client.list_models()
            return any('groq' in str(m.get('provider', '')).lower() for m in models)
        except Exception:
            return False
    
    def chat(self, prompt: str, **kwargs) -> str:
        """Forward to sovereign gateway. Returns text for backward compatibility."""
        agent = kwargs.get('agent', 'core_legacy')
        try:
            response = self.client.call_sync(
                prompt=prompt,
                agent=agent,
            )
            return response.content
        except Exception as e:
            raise RuntimeError(
                f"SOVEREIGN GATEWAY FAILURE in core/llm_manager: "
                f"The throne is unreachable. Underlying error: {e}"
            ) from e
    
    def chat_sync(self, prompt: str, **kwargs) -> str:
        """Alias for chat() — many agents call this method name."""
        return self.chat(prompt, **kwargs)
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Another alias — some agents use this method name."""
        return self.chat(prompt, **kwargs)
    
    def __getattr__(self, name):
        """Proxy unknown attributes to the sovereign client.
        
        This catches legacy patterns like self.llm.some_obscure_method
        and routes them through the gateway when possible.
        """
        # Prevent infinite recursion
        if name.startswith('_'):
            raise AttributeError(name)
        try:
            return getattr(self.client, name)
        except AttributeError:
            raise AttributeError(
                f"LLMManager adapter has no attribute '{name}'. "
                f"The sovereign gateway also lacks this attribute. "
                f"Update calling code to use shared.llm directly."
            )


def get_llm_manager():
    """Factory function — preserved for backward compatibility.
    
    Returns an adapter that delegates to the sovereign gateway.
    All existing callers continue to work unchanged.
    """
    return LLMManager()