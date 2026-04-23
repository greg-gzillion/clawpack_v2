"""HTTP hook runner - webhook calls"""
from typing import Dict, Optional
import aiohttp
from ..hook_types import HookResult, HookContext

class HttpRunner:
    """Execute hooks as HTTP webhooks"""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
    
    async def run(self, url: str, context: HookContext, input_data: Optional[Dict] = None) -> HookResult:
        """Run an HTTP hook"""
        try:
            payload = {
                "event": context.event.value,
                "tool_name": context.tool_name,
                "tool_input": input_data,
                "session_id": context.session_id,
                "agent_id": context.agent_id,
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=payload,
                    timeout=self.timeout,
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return HookResult(
                            allowed=data.get("allowed", True),
                            block=not data.get("allowed", True),
                            modified_input=data.get("modified_input"),
                            additional_context=data.get("additional_context"),
                            reason=data.get("reason"),
                        )
                    else:
                        text = await response.text()
                        return HookResult(
                            allowed=False,
                            block=True,
                            reason=f"HTTP {response.status}: {text}",
                        )
        except Exception as e:
            return HookResult(allowed=False, block=True, reason=str(e))
