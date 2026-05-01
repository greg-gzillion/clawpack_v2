"""Provider Registry - Now routes through the sovereign gateway.

   CONSTITUTIONAL UPDATE: MedicLaw no longer maintains its own provider system.
   All model access now routes through shared/llm/client.py — the one throne.
   
   This file is now an ADAPTER, not an authority.
   It translates mediclaw's interface to the sovereign gateway's interface.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class ProviderRegistry:
    """ADAPTER ONLY — Routes all mediclaw LLM calls through the sovereign gateway.
    
    This is NOT a provider system. It has no independent authority.
    It delegates entirely to shared/llm/client.py for:
    - Provider selection
    - Fallback routing  
    - Budget enforcement
    - Chronicle audit
    - Model registry
    """
    
    def __init__(self):
        self._client = None
        self.providers = []  # Preserved for backward compatibility
        print("✅ MedicLaw Provider Registry — routing through sovereign gateway")
    
    @property
    def client(self):
        """THE SOVEREIGN GATEWAY — All model access passes through here."""
        if self._client is None:
            from shared.llm import get_llm_client
            self._client = get_llm_client()
        return self._client
    
    def get_available(self):
        """Return available providers from the sovereign registry."""
        models = self.client.list_models()
        return [m['name'] for m in models]
    
    def generate(self, prompt: str) -> tuple:
        """Generate text through the sovereign gateway.
        
        Returns (result_text, provider_name) for backward compatibility.
        """
        try:
            response = self.client.call_sync(
                prompt=prompt,
                agent="mediclaw",
                capability="medical_analysis",
            )
            return response.content, response.provider.value
        except Exception as e:
            raise RuntimeError(
                f"SOVEREIGN GATEWAY FAILURE in mediclaw: The throne is unreachable. "
                f"No model access is possible without constitutional authority. "
                f"Underlying error: {e}"
            ) from e