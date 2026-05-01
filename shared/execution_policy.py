"""Execution Policy — Hard boundaries for all agents.

   CONSTITUTIONAL LAW: Agents must not perform destructive actions
   without explicit approval. This is not a prompt. This is code.
   
   This file defines what agents are PERMITTED to do.
   It is the executive constitution of Clawpack V2.
"""
from enum import Enum
from typing import Dict, Callable, Optional


class ApprovalLevel(Enum):
    ALLOWED = "allowed"
    RESTRICTED = "restricted" 
    REQUIRE_APPROVAL = "require_approval"
    BLOCKED = "blocked"


class ExecutionPolicy:
    """Hard boundaries for agent actions. Enforced in code, not prompts."""

    # File system
    ALLOW_READ = True
    ALLOW_WRITE = True
    ALLOW_DELETE = False
    ALLOW_EXECUTE = False

    # Version control
    ALLOW_GIT_COMMIT = ApprovalLevel.REQUIRE_APPROVAL
    ALLOW_GIT_PUSH = ApprovalLevel.REQUIRE_APPROVAL
    ALLOW_GIT_FORCE_PUSH = ApprovalLevel.BLOCKED

    # Network
    ALLOW_HTTP_REQUEST = True
    ALLOW_API_KEY_USAGE = True  # Routed through sovereign gateway
    ALLOW_NETWORK_PUSH = ApprovalLevel.REQUIRE_APPROVAL
    ALLOW_DOWNLOAD_FILE = ApprovalLevel.REQUIRE_APPROVAL

    # Database
    ALLOW_DB_READ = True
    ALLOW_DB_WRITE = True
    ALLOW_DB_DESTRUCTIVE = ApprovalLevel.BLOCKED
    ALLOW_DB_SCHEMA_CHANGE = ApprovalLevel.REQUIRE_APPROVAL

    # System
    ALLOW_SUBPROCESS = ApprovalLevel.RESTRICTED
    ALLOW_SHELL_COMMANDS = ApprovalLevel.BLOCKED
    ALLOW_ENV_MODIFICATION = ApprovalLevel.REQUIRE_APPROVAL

    # Agent actions
    ALLOW_DELEGATION = True
    ALLOW_AGENT_SPAWN = ApprovalLevel.REQUIRE_APPROVAL
    ALLOW_SELF_MODIFY = ApprovalLevel.BLOCKED

    @classmethod
    def check(cls, action: str, context: dict = None) -> Dict:
        """Check if an action is permitted.
        
        Returns dict with allowed, level, reason.
        """
        policy = getattr(cls, action, None)
        
        if policy is None:
            return {"allowed": False, "level": ApprovalLevel.BLOCKED, "reason": f"Unknown action: {action}"}
        
        if policy is True:
            return {"allowed": True, "level": ApprovalLevel.ALLOWED, "reason": "Explicitly permitted"}
        
        if policy is False:
            return {"allowed": False, "level": ApprovalLevel.BLOCKED, "reason": "Explicitly blocked"}
        
        if isinstance(policy, ApprovalLevel):
            if policy == ApprovalLevel.ALLOWED:
                return {"allowed": True, "level": policy, "reason": "Permitted by policy"}
            elif policy == ApprovalLevel.BLOCKED:
                return {"allowed": False, "level": policy, "reason": "Blocked by policy"}
            elif policy == ApprovalLevel.REQUIRE_APPROVAL:
                return {"allowed": False, "level": policy, "reason": "Requires explicit approval"}
            elif policy == ApprovalLevel.RESTRICTED:
                return {"allowed": False, "level": policy, "reason": "Restricted — limited circumstances only"}
        
        return {"allowed": False, "level": ApprovalLevel.BLOCKED, "reason": "Policy check failed"}

    @classmethod
    def request_approval(cls, action: str, details: str = "") -> bool:
        """Request human approval for a restricted action.
        
        In production, this should integrate with an approval queue.
        For now, it logs and returns False (deny by default).
        """
        print(f"APPROVAL REQUIRED: {action}")
        if details:
            print(f"  Details: {details}")
        print(f"  Auto-denied. Human approval not configured.")
        return False

    @classmethod
    def list_policies(cls) -> Dict:
        """List all policies and their current values."""
        policies = {}
        for attr in dir(cls):
            if attr.startswith("ALLOW_"):
                val = getattr(cls, attr)
                if isinstance(val, ApprovalLevel):
                    policies[attr] = val.value
                else:
                    policies[attr] = str(val)
        return policies


__all__ = ["ExecutionPolicy", "ApprovalLevel"]