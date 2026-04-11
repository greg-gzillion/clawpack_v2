"""Lifecycle hooks for agent operations - inspired by rustclaw"""

from enum import Enum
from typing import Dict, Any, Callable
from functools import wraps

class HookPoint(Enum):
    BEFORE_INBOUND = "before_inbound"
    BEFORE_TOOL_CALL = "before_tool_call"
    BEFORE_OUTBOUND = "before_outbound"
    ON_SESSION_START = "on_session_start"
    ON_SESSION_END = "on_session_end"
    TRANSFORM_RESPONSE = "transform_response"

class HookManager:
    """Manage lifecycle hooks for agents"""
    
    def __init__(self):
        self.hooks = {hook: [] for hook in HookPoint}
    
    def register(self, hook_point: HookPoint, callback: Callable):
        """Register a hook callback"""
        self.hooks[hook_point].append(callback)
    
    def execute(self, hook_point: HookPoint, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute all hooks at a point"""
        result = context
        for hook in self.hooks[hook_point]:
            result = hook(result)
        return result

# Global hook manager
hook_manager = HookManager()

def hook(hook_point: HookPoint):
    """Decorator to register a function as a hook"""
    def decorator(func):
        hook_manager.register(hook_point, func)
        return func
    return decorator
