"""
CONSTITUTIONAL UPDATE: RustyPyCraw no longer maintains its own Groq client.
All model access now routes through shared/llm/client.py — the sovereign gateway.

This was a shadow treasury — own API keys, own model selection, zero governance.
Now it's an adapter that demonstrates constitutional compliance.
Every code analysis is audited, budgeted, and governed.
"""

import sys
import os
import warnings
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

warnings.warn(
    "rustypycraw/modules/llm/groq_client.py is DEPRECATED as an independent authority. "
    "All model access must route through shared/llm/client.py. "
    "This adapter will be removed once all code analysis routes through sovereignty.",
    DeprecationWarning,
    stacklevel=2
)

__all__ = ["GroqClient"]  # Predictable transition


class GroqClient:
    """ADAPTER ONLY — Delegates all LLM calls to the sovereign gateway.
    
    This is NOT a Groq client. It has no independent authority.
    All API key management, model selection, and provider routing
    is handled by shared/llm/client.py — the single point of model access.
    
    Preserved for backward compatibility during constitutional transition.
    """
    
    def __init__(self, api_key=None, model=None):
        self._client = None
        # Preserved for backward compatibility — no longer functional
        self.api_key = api_key  # Sovereign handles credentials
        self.model = model      # Sovereign handles model selection
        self.max_retries = 3    # Constitutional budget law: cap recursive analysis
        self.max_retry_cost = 0.25  # Constitutional cost ceiling
        print("⚠️ GroqClient is now an adapter — routing through sovereign gateway")
    
    @property
    def client(self):
        """THE SOVEREIGN GATEWAY — All model access passes through here."""
        if self._client is None:
            from shared.llm import get_llm_client
            self._client = get_llm_client()
        return self._client
    
    def chat_completion(self, messages, model=None, **kwargs):
        """Generate chat completion through the sovereign gateway.
        
        Preserves the Groq-like interface for backward compatibility.
        All calls are audited, budgeted, and governed.
        
        Args:
            messages: List of message dicts or string prompt
            model: Ignored — sovereign handles model selection via llmclaw /use
            **kwargs: Preserved for compatibility
            
        Returns:
            Dict with full audit metadata
        """
        # Extract prompt from messages
        if isinstance(messages, list):
            prompt = messages[-1].get('content', str(messages)) if messages else ""
        else:
            prompt = str(messages)
        
        # Build audit trail for recursive code analysis
        audit_trail = []
        total_cost = 0.0
        
        for attempt in range(self.max_retries):
            try:
                response = self.client.call_sync(
                    prompt=prompt,
                    agent="rustypycraw",
                    capability="code_analysis" if attempt == 0 else "code_analysis_refinement",
                )
                
                audit_entry = {
                    'attempt': attempt + 1,
                    'model': response.model,
                    'provider': response.provider.value,
                    'tokens': response.tokens_used,
                    'cost': response.cost,
                    'audit_hash': response.request_hash,
                    'timestamp': response.timestamp,
                }
                audit_trail.append(audit_entry)
                total_cost += response.cost
                
                # Constitutional cost ceiling — prevent runaway spending
                if total_cost > self.max_retry_cost:
                    return {
                        'content': f"Code analysis cost ceiling reached (${total_cost:.4f}). Audit trail: {audit_trail}",
                        'model': 'governance',
                        'provider': 'sovereign',
                        'tokens': 0,
                        'cost': total_cost,
                        'audit_hash': 'COST_CEILING',
                        'audit_trail': audit_trail,
                    }
                
                # Return successful response with full governance metadata
                return {
                    'content': response.content,
                    'model': response.model,
                    'provider': response.provider.value,
                    'tokens': response.tokens_used,
                    'cost': response.cost,
                    'audit_hash': response.request_hash,
                    'audit_trail': audit_trail,
                    'total_cost': total_cost,
                }
                
            except Exception as e:
                audit_trail.append({
                    'attempt': attempt + 1,
                    'error': str(e),
                    'cost': 0,
                })
                
                if attempt == self.max_retries - 1:
                    raise RuntimeError(
                        f"SOVEREIGN GATEWAY FAILURE in rustypycraw: "
                        f"All {self.max_retries} code analysis attempts failed. "
                        f"Audit trail: {audit_trail}"
                    ) from e
        
        # Should never reach here due to the raise above
        return {
            'content': f"Code analysis failed after {self.max_retries} attempts",
            'model': 'governance',
            'provider': 'sovereign',
            'tokens': 0,
            'cost': total_cost,
            'audit_hash': 'MAX_RETRIES',
            'audit_trail': audit_trail,
        }
    
    def is_available(self) -> bool:
        """Delegate truthfully — never mask constitutional failures."""
        try:
            return len(self.client.list_models()) > 0
        except Exception:
            return False
    
    def list_models(self) -> list:
        """List available models from the sovereign registry.
        
        Returns models the sovereign gateway can access, not just Groq models.
        """
        return self.client.list_models()
    
    def get_usage_stats(self) -> dict:
        """Get RustyPyCraw-specific usage statistics from Chronicle."""
        try:
            stats = self.client.get_stats()
            return {
                'code_analyses': stats.get('by_agent', {}).get('rustypycraw', 0),
                'analysis_cost': stats.get('cost_by_agent', {}).get('rustypycraw', 0.0),
                'sovereign_gateway': True,
            }
        except Exception:
            return {
                'code_analyses': 0,
                'analysis_cost': 0.0,
                'sovereign_gateway': False,
                'error': 'Chronicle unreachable'
            }