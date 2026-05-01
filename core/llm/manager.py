"""ADAPTER — core/llm/manager.py now delegates to the sovereign gateway.

   CONSTITUTIONAL UPDATE: This was the original LLM Manager—the intended
   central authority that agents bypassed. Now it becomes an adapter to
   the real throne: shared/llm/client.py.

   All provider discovery, fallback routing, model selection, audit logging,
   and budget enforcement are handled by the sovereign gateway.
   
   This file exists to prevent breakage during constitutional transition.
   New code should import from shared.llm directly.
"""

import warnings

warnings.warn(
    "core/llm/manager.py is DEPRECATED as an authority. "
    "It now delegates to shared/llm/client.py — the sovereign gateway. "
    "Import from shared.llm directly in new code.",
    DeprecationWarning,
    stacklevel=2
)

__all__ = ['get_manager', 'Manager']


class Manager:
    """ADAPTER ONLY — Delegates all LLM calls to the sovereign gateway.
    
    This is NOT a model manager. It has no independent authority.
    Provider discovery, fallback, audit, and budget are all handled
    by shared/llm/client.py — the single point of model access.
    """
    
    def __init__(self):
        self._client = None
        self.providers = []  # Preserved for compatibility
        self.cache = None    # Preserved for compatibility
        self._groq = True    # Sovereign handles provider routing
    
    @property
    def client(self):
        """THE SOVEREIGN GATEWAY — All model access passes through here."""
        if self._client is None:
            from shared.llm import get_llm_client
            self._client = get_llm_client()
        return self._client
    
    def chat(self, prompt: str, agent: str = None, task: str = None) -> str:
        """Route through sovereign gateway.
        
        The sovereign handles provider selection, fallback, and routing.
        Agent and task parameters are preserved for audit trail.
        """
        try:
            response = self.client.call_sync(
                prompt=prompt,
                agent=agent or "core_legacy",
                capability=task or "general",
            )
            return response.content
        except Exception as e:
            raise RuntimeError(
                f"SOVEREIGN GATEWAY FAILURE in core/llm/manager: "
                f"The throne is unreachable. Underlying error: {e}"
            ) from e
    
    def status(self) -> dict:
        """Delegate status check to sovereign gateway."""
        try:
            stats = self.client.get_stats()
            models = self.client.list_models()
            return {
                "total": len(models),
                "working": len(models),
                "groq": any('groq' in str(m.get('provider', '')).lower() for m in models),
                "sovereign": True,
                "total_interactions": stats.get('total_interactions', 0),
                "total_cost": stats.get('total_cost', 0.0),
            }
        except Exception:
            return {
                "total": 0,
                "working": 0,
                "groq": False,
                "sovereign": False,
                "error": "Sovereign gateway unreachable"
            }
    
    def list(self) -> str:
        """Delegate model listing to sovereign registry."""
        try:
            models = self.client.list_models()
            if not models:
                return "No models available via sovereign gateway"
            lines = [f"Available models ({len(models)}) — governed by shared/llm:"]
            for m in models:
                name = m.get('name', 'unknown')
                provider = m.get('provider', 'unknown')
                tier = m.get('tier', 'standard')
                obliterated = "⚡" if m.get('is_obliterated') else " "
                lines.append(f"  [{obliterated}] {name} ({provider}) [{tier}]")
            return "\n".join(lines)
        except Exception:
            return "Sovereign gateway unreachable — no model listing available"


_manager = None

def get_manager() -> Manager:
    """Factory function — preserved for backward compatibility.
    
    Returns an adapter that delegates to the sovereign gateway.
    """
    global _manager
    if _manager is None:
        _manager = Manager()
    return _manager