"""DEPRECATED — Ollama provider for MedicLaw.

   CONSTITUTIONAL VIOLATION: This file maintained independent model access.
   All calls now route through shared/llm/client.py — the sovereign gateway.
   
   This file exists only for backward compatibility during transition.
   DO NOT import this directly. Use ProviderRegistry or shared.llm directly.
"""
import warnings

warnings.warn(
    "mediclaw/providers/ollama.py is DEPRECATED. "
    "All model access must route through shared/llm/client.py. "
    "This file will be removed.",
    DeprecationWarning,
    stacklevel=2
)

# Delegate to sovereign gateway
from shared.llm.client import get_llm_client

class OllamaProvider:
    """ADAPTER ONLY — Delegates to sovereign gateway."""
    
    def __init__(self):
        self._client = get_llm_client()
        self.name = "ollama"
    
    def is_available(self):
        return True  # Sovereign handles actual availability
    
    def generate(self, prompt):
        response = self._client.call_sync(
            prompt=prompt,
            agent="mediclaw",
            capability="medical_analysis",
        )
        return response.content