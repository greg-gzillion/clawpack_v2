"""
CONSTITUTIONAL UPDATE: MathematicaClaw visualizer now routes through sovereign gateway.

This was a recursive stealth spender — generating prompts, calling models,
retrying for formatting, performing hidden iterative refinement with zero audit trail.
Now every call is governed, budgeted, and traceable through shared/llm/client.py.

No visualization is generated without the throne's knowledge.
"""

import sys
import warnings
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

warnings.warn(
    "mathematicaclaw/ai_visualizer.py is DEPRECATED as an independent authority. "
    "All model access now routes through shared/llm/client.py. "
    "Visualizations are generated with full audit trail and budget enforcement.",
    DeprecationWarning,
    stacklevel=2
)

__all__ = ["AIVisualizer"]


class AIVisualizer:
    """ADAPTER ONLY — All LLM calls route through the sovereign gateway.
    
    This is NOT an independent visualizer. It has no direct model access.
    Every visualization prompt, refinement, and retry is:
    - Logged to Chronicle with audit metadata
    - Subject to budget enforcement
    - Controlled by llmclaw /use for model selection
    - Traceable by request_hash for debugging
    """
    
    def __init__(self):
        self._client = None
        self.max_retries = 3  # Limit recursive spending
        print("✅ AIVisualizer initialized — routing through sovereign gateway")
    
    @property
    def client(self):
        """THE SOVEREIGN GATEWAY — All model access passes through here."""
        if self._client is None:
            from shared.llm import get_llm_client
            self._client = get_llm_client()
        return self._client
    
    def visualize_math(self, expression: str, method: str = "auto") -> dict:
        """Generate mathematical visualization through sovereign gateway.
        
        All prompts, refinements, and retries are audited.
        Recursive spending is capped at max_retries.
        
        Returns dict with visualization code and full audit trail.
        """
        prompt = self._build_prompt(expression, method)
        audit_trail = []
        
        for attempt in range(self.max_retries):
            try:
                response = self.client.call_sync(
                    prompt=prompt,
                    agent="mathematicaclaw",
                    capability="math_visualization",
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
                
                # Parse and validate the response
                viz_data = self._parse_visualization(response.content)
                
                if viz_data and self._validate_visualization(viz_data):
                    return {
                        'visualization': viz_data,
                        'expression': expression,
                        'method': method,
                        'audit_trail': audit_trail,
                        'total_attempts': attempt + 1,
                        'total_cost': sum(e['cost'] for e in audit_trail),
                        'final_model': response.model,
                    }
                
                # If validation failed, refine the prompt with error context
                if attempt < self.max_retries - 1:
                    prompt = self._build_refinement_prompt(
                        expression, method, 
                        response.content, 
                        "Validation failed — improve output format"
                    )
                    
            except Exception as e:
                audit_trail.append({
                    'attempt': attempt + 1,
                    'error': str(e),
                    'cost': 0,
                })
                
                if attempt == self.max_retries - 1:
                    raise RuntimeError(
                        f"SOVEREIGN GATEWAY FAILURE in mathematicaclaw visualizer: "
                        f"All {self.max_retries} attempts failed. "
                        f"Audit trail: {audit_trail}"
                    ) from e
        
        # Max retries exceeded
        return {
            'visualization': None,
            'expression': expression,
            'method': method,
            'audit_trail': audit_trail,
            'total_attempts': self.max_retries,
            'total_cost': sum(e.get('cost', 0) for e in audit_trail),
            'error': f"Failed after {self.max_retries} sovereign attempts",
        }
    
    def _build_prompt(self, expression: str, method: str) -> str:
        """Build visualization prompt — no model access here, just text."""
        return f"""Generate a mathematical visualization for: {expression}
Method: {method}
Output format: ASCII/Unicode art with mathematical notation
Requirements: Accurate, clear, properly formatted"""
    
    def _build_refinement_prompt(self, expression: str, method: str, 
                                  previous_output: str, error: str) -> str:
        """Build refinement prompt for retry — audited like any other call."""
        return f"""Previous visualization attempt for '{expression}' using {method} failed: {error}

Previous output:
{previous_output}

Please regenerate with corrected formatting and accurate mathematical representation."""
    
    def _parse_visualization(self, content: str):
        """Parse visualization from response — no model access."""
        # Preserved from original implementation
        try:
            # Extract the visualization content
            if '```' in content:
                lines = content.split('\n')
                code_lines = []
                in_block = False
                for line in lines:
                    if line.startswith('```'):
                        in_block = not in_block
                        continue
                    if in_block:
                        code_lines.append(line)
                return '\n'.join(code_lines) if code_lines else content
            return content
        except Exception:
            return content
    
    def _validate_visualization(self, viz_data) -> bool:
        """Validate visualization output — no model access."""
        if not viz_data or len(str(viz_data).strip()) < 10:
            return False
        # Basic validation: must contain some mathematical notation or structure
        math_indicators = ['+', '-', '*', '/', '=', '∑', '∫', '√', '(', '[', '{', '|']
        return any(indicator in str(viz_data) for indicator in math_indicators)
    
    def get_usage_stats(self) -> dict:
        """Get visualization-specific usage statistics."""
        try:
            stats = self.client.get_stats()
            return {
                'visualizations_generated': stats.get('by_agent', {}).get('mathematicaclaw', 0),
                'visualization_cost': stats.get('cost_by_agent', {}).get('mathematicaclaw', 0.0),
                'sovereign_gateway': True,
            }
        except Exception:
            return {
                'visualizations_generated': 0,
                'visualization_cost': 0.0,
                'sovereign_gateway': False,
                'error': 'Chronicle unreachable'
            }