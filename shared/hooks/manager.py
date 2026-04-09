"""Hook manager - Main interface for hook system"""

import asyncio
from typing import Optional, Dict, Any
from pathlib import Path

from .types import HookPoint, HookContext, HookResult, HookConfig
from .loader import HookLoader
from .executor import HookExecutor


class HookManager:
    """Central manager for the hooks system"""
    
    def __init__(self, agent_name: str, session_id: str, workspace_trusted: bool = False):
        self.agent_name = agent_name
        self.session_id = session_id
        self.workspace_trusted = workspace_trusted
        
        self.loader = HookLoader()
        self.executor = HookExecutor(workspace_trusted)
        
        # Load and freeze configs at startup (snapshot security)
        self._initialize()
        
        # Track executed hooks
        self._execution_history: list = []
    
    def _initialize(self):
        """Load and freeze hook configurations"""
        configs = self.loader.load_all()
        self.executor.freeze_configs(configs)
        
        print(f"📎 Loaded {len(configs)} hooks")
    
    def create_example_hooks(self):
        """Create example hooks for customization"""
        self.loader.create_example_hooks()
    
    async def execute(
        self,
        hook_point: HookPoint,
        tool_name: Optional[str] = None,
        tool_arguments: Optional[Dict[str, Any]] = None,
        tool_result: Optional[Any] = None,
        tool_error: Optional[str] = None,
        user_input: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> HookResult:
        """
        Execute hooks for a lifecycle point.
        
        Returns HookResult with:
        - exit_code: SUCCESS, BLOCK, or WARNING
        - message: User-facing message
        - modified_input: Modified tool arguments (if any)
        - permission_decision: 'allow', 'deny', or 'ask'
        """
        context = HookContext(
            hook_point=hook_point,
            agent_name=self.agent_name,
            session_id=self.session_id,
            tool_name=tool_name,
            tool_arguments=tool_arguments,
            tool_result=tool_result,
            tool_error=tool_error,
            user_input=user_input,
            metadata=metadata or {}
        )
        
        result = await self.executor.execute_hooks(hook_point, context)
        
        # Track execution
        self._execution_history.append({
            'hook_point': hook_point.value,
            'result': result.exit_code.value,
            'message': result.message
        })
        
        return result
    
    # Convenience methods for each hook point
    async def pre_tool_use(self, tool_name: str, arguments: Dict[str, Any]) -> HookResult:
        """Execute PreToolUse hooks"""
        return await self.execute(
            HookPoint.PRE_TOOL_USE,
            tool_name=tool_name,
            tool_arguments=arguments
        )
    
    async def post_tool_use(self, tool_name: str, arguments: Dict[str, Any], result: Any) -> HookResult:
        """Execute PostToolUse hooks"""
        return await self.execute(
            HookPoint.POST_TOOL_USE,
            tool_name=tool_name,
            tool_arguments=arguments,
            tool_result=result
        )
    
    async def user_prompt_submit(self, user_input: str) -> HookResult:
        """Execute UserPromptSubmit hooks"""
        return await self.execute(
            HookPoint.USER_PROMPT_SUBMIT,
            user_input=user_input
        )
    
    async def session_start(self) -> HookResult:
        """Execute SessionStart hooks"""
        return await self.execute(HookPoint.SESSION_START)
    
    async def session_end(self) -> HookResult:
        """Execute SessionEnd hooks"""
        return await self.execute(HookPoint.SESSION_END)
    
    async def stop(self) -> HookResult:
        """Execute Stop hooks"""
        return await self.execute(HookPoint.STOP)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get hook execution statistics"""
        return {
            'total_hooks': len(self.executor._frozen_configs),
            'executions': len(self._execution_history),
            'history': self._execution_history[-10:]  # Last 10
        }
