"""Permission System - Claude Code Pattern #6"""
from enum import Enum
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from pathlib import Path
import json

class PermissionMode(Enum):
    """Seven permission modes, ordered most to least permissive"""
    BYPASS = "bypass"           # Everything allowed, no checks
    DONT_ASK = "dont_ask"       # All allowed, still logged
    AUTO = "auto"               # LLM classifier decides
    ACCEPT_EDITS = "accept_edits"  # File edits auto-approved
    DEFAULT = "default"         # Standard interactive
    PLAN = "plan"               # Read-only, all mutations blocked
    BUBBLE = "bubble"           # Escalate to parent

class RuleBehavior(Enum):
    """Permission rule behaviors"""
    ALLOW = "allow"
    DENY = "deny"
    ASK = "ask"

@dataclass
class PermissionRule:
    """A single permission rule"""
    tool_name: str
    behavior: RuleBehavior
    content_pattern: Optional[str] = None  # e.g., "git *" or "/src/**"
    source: str = "user"  # user, project, policy, session
    
    def matches(self, tool: str, input_data: Dict) -> bool:
        """Check if rule matches tool call"""
        if tool != self.tool_name and self.tool_name != "*":
            return False
        
        if self.content_pattern:
            # Simple pattern matching - can be enhanced
            cmd = str(input_data.get("command", ""))
            pattern = self.content_pattern.replace("*", ".*")
            import re
            return bool(re.search(pattern, cmd))
        
        return True

@dataclass
class PermissionRequest:
    """A permission request"""
    tool_name: str
    tool_input: Dict[str, Any]
    tool_use_id: str
    description: str
    suggested_behavior: RuleBehavior = RuleBehavior.ASK

@dataclass
class PermissionResult:
    """Result of permission check"""
    allowed: bool
    behavior: RuleBehavior
    reason: str
    requires_prompt: bool = False
    modified_input: Optional[Dict] = None

class PermissionSystem:
    """Central permission system"""
    
    def __init__(self, mode: PermissionMode = PermissionMode.DEFAULT):
        self.mode = mode
        self.rules: List[PermissionRule] = []
        self.history: List[PermissionRequest] = []
        self.denied_tools: set = set()  # Session-scoped denials
        
        # Load default rules
        self._load_default_rules()
    
    def _load_default_rules(self):
        """Load built-in safety rules"""
        # Always allow read-only tools in plan mode
        self.add_rule(PermissionRule(
            tool_name="*",
            behavior=RuleBehavior.ALLOW,
            content_pattern=None,
            source="builtin"
        ))
        
        # Dangerous commands always ask
        dangerous = ["rm", "sudo", "chmod", "chown", "dd", "mkfs"]
        for cmd in dangerous:
            self.add_rule(PermissionRule(
                tool_name="bash",
                behavior=RuleBehavior.ASK,
                content_pattern=f"{cmd} *",
                source="builtin"
            ))
    
    def add_rule(self, rule: PermissionRule):
        """Add a permission rule"""
        self.rules.append(rule)
    
    def set_mode(self, mode: PermissionMode):
        """Change permission mode"""
        self.mode = mode
        print(f"🔒 Permission mode: {mode.value}")
    
    def check(self, tool_name: str, tool_input: Dict[str, Any]) -> PermissionResult:
        """Check if tool execution is allowed"""
        
        # Mode-based overrides
        if self.mode == PermissionMode.BYPASS:
            return PermissionResult(True, RuleBehavior.ALLOW, "Bypass mode")
        
        if self.mode == PermissionMode.PLAN:
            # In plan mode, only allow read-only tools
            read_only = {"read", "grep", "glob", "search", "webclaw", "mathematicaclaw", "interpretclaw"}
            if tool_name not in read_only:
                return PermissionResult(False, RuleBehavior.DENY, "Plan mode: write operations blocked")
            return PermissionResult(True, RuleBehavior.ALLOW, "Plan mode: read operation")
        
        if self.mode == PermissionMode.DONT_ASK:
            return PermissionResult(True, RuleBehavior.ALLOW, "Don't ask mode")
        
        # Check if tool was denied this session
        if tool_name in self.denied_tools:
            return PermissionResult(False, RuleBehavior.DENY, f"Tool {tool_name} denied this session")
        
        # Check rules (last matching wins)
        matched_rule = None
        for rule in self.rules:
            if rule.matches(tool_name, tool_input):
                matched_rule = rule
        
        if matched_rule:
            if matched_rule.behavior == RuleBehavior.ALLOW:
                return PermissionResult(True, RuleBehavior.ALLOW, f"Rule: {matched_rule.source}")
            elif matched_rule.behavior == RuleBehavior.DENY:
                self.denied_tools.add(tool_name)
                return PermissionResult(False, RuleBehavior.DENY, f"Rule: {matched_rule.source}")
            elif matched_rule.behavior == RuleBehavior.ASK:
                return PermissionResult(True, RuleBehavior.ASK, "Rule requires approval", requires_prompt=True)
        
        # Default: ask for write operations
        write_tools = {"write", "edit", "bash", "rm", "mv", "cp"}
        if tool_name in write_tools:
            return PermissionResult(True, RuleBehavior.ASK, "Write operation", requires_prompt=True)
        
        return PermissionResult(True, RuleBehavior.ALLOW, "Default allow")
    
    def request_permission(self, request: PermissionRequest) -> PermissionResult:
        """Request permission with interactive prompt"""
        self.history.append(request)
        
        result = self.check(request.tool_name, request.tool_input)
        
        if result.requires_prompt:
            # Interactive prompt
            print(f"\n🔐 Permission Required:")
            print(f"   Tool: {request.tool_name}")
            print(f"   Description: {request.description}")
            print(f"   Input: {str(request.tool_input)[:100]}...")
            
            response = input("   Allow? [y/N/a(ll)/d(eny session)]: ").strip().lower()
            
            if response == 'a':
                # Add temporary allow rule
                self.add_rule(PermissionRule(
                    tool_name=request.tool_name,
                    behavior=RuleBehavior.ALLOW,
                    source="session"
                ))
                return PermissionResult(True, RuleBehavior.ALLOW, "User allowed all")
            elif response == 'd':
                self.denied_tools.add(request.tool_name)
                return PermissionResult(False, RuleBehavior.DENY, "User denied session")
            elif response == 'y':
                return PermissionResult(True, RuleBehavior.ALLOW, "User allowed")
            else:
                return PermissionResult(False, RuleBehavior.DENY, "User denied")
        
        return result
    
    def log_permission(self, request: PermissionRequest, result: PermissionResult):
        """Log permission decision for audit"""
        log_entry = {
            "timestamp": str(__import__('datetime').datetime.now()),
            "tool": request.tool_name,
            "input": str(request.tool_input)[:200],
            "allowed": result.allowed,
            "reason": result.reason,
            "mode": self.mode.value
        }
        
        # Write to audit log
        log_file = Path("data/permissions.jsonl")
        log_file.parent.mkdir(exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def get_stats(self) -> Dict:
        """Get permission statistics"""
        allowed = sum(1 for r in self.history if self.check(r.tool_name, r.tool_input).allowed)
        denied = len(self.history) - allowed
        
        return {
            "mode": self.mode.value,
            "total_requests": len(self.history),
            "allowed": allowed,
            "denied": denied,
            "denied_tools": list(self.denied_tools),
            "rules_count": len(self.rules)
        }

# Global permission system instance
_permission_system = None

def get_permission_system(mode: PermissionMode = None) -> PermissionSystem:
    """Get or create global permission system"""
    global _permission_system
    if _permission_system is None:
        _permission_system = PermissionSystem(mode or PermissionMode.DEFAULT)
    elif mode:
        _permission_system.set_mode(mode)
    return _permission_system
