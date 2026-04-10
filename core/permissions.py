"""Permission modes - inspired by Claude Code"""
from enum import Enum
from typing import Dict, Any

class PermissionMode(Enum):
    BYPASS = "bypass"  # Everything allowed
    DONT_ASK = "dont_ask"  # All allowed, no prompts
    AUTO = "auto"  # LLM decides
    ACCEPT_EDITS = "accept_edits"  # Edits auto, others prompt
    DEFAULT = "default"  # User approves each
    PLAN = "plan"  # Read-only
    BUBBLE = "bubble"  # Escalate to parent

class PermissionSystem:
    def __init__(self, mode: PermissionMode = PermissionMode.DEFAULT):
        self.mode = mode
        self.parent = None
    
    def can_execute(self, tool_name: str, args: Dict) -> tuple[bool, str]:
        """Check if tool can execute in current mode"""
        
        if self.mode == PermissionMode.BYPASS:
            return True, "Bypassed"
        
        if self.mode == PermissionMode.PLAN:
            if tool_name in ['read', 'list', 'search']:
                return True, "Read-only allowed"
            return False, "Plan mode blocks mutations"
        
        if self.mode == PermissionMode.ACCEPT_EDITS:
            if tool_name in ['write', 'edit', 'patch']:
                return True, "Edits auto-approved"
            return self._ask_user(tool_name, args)
        
        if self.mode == PermissionMode.DEFAULT:
            return self._ask_user(tool_name, args)
        
        if self.mode == PermissionMode.BUBBLE:
            if self.parent:
                return self.parent.can_execute(tool_name, args)
            return False, "No parent to escalate to"
        
        return True, "Allowed"
    
    def _ask_user(self, tool_name: str, args: Dict) -> tuple[bool, str]:
        """Interactive user prompt"""
        response = input(f"\n🔐 Allow {tool_name} with {args}? [y/N]: ")
        if response.lower() == 'y':
            return True, "User approved"
        return False, "User denied"
