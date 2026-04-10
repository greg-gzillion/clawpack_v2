"""Prompt hook runner - single LLM call"""
from typing import Dict, Optional
from ..hook_types import HookResult, HookContext

class PromptRunner:
    """Execute hooks as single LLM prompts"""
    
    def __init__(self, llm_manager=None):
        self.llm_manager = llm_manager
    
    async def run(self, prompt: str, context: HookContext, input_data: Optional[Dict] = None) -> HookResult:
        """Run a prompt hook"""
        # Build prompt
        full_prompt = f"""{prompt}

Tool: {context.tool_name}
Input: {input_data}
Session: {context.session_id}

Respond with JSON: {{"allowed": true/false, "reason": "..."}}"""
        
        try:
            if self.llm_manager and hasattr(self.llm_manager, 'chat_sync'):
                response = self.llm_manager.chat_sync(full_prompt)
                # Parse response (simplified)
                import json
                if '{' in response:
                    data = json.loads(response[response.index('{'):response.rindex('}')+1])
                    return HookResult(
                        allowed=data.get("allowed", True),
                        block=not data.get("allowed", True),
                        reason=data.get("reason"),
                        additional_context=data.get("context"),
                    )
        except Exception as e:
            return HookResult(allowed=False, block=True, reason=str(e))
        
        return HookResult(allowed=True)
