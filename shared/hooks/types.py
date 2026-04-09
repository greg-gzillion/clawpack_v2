"""Hook type definitions"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime


class HookPoint(str, Enum):
    """Lifecycle points where hooks can fire"""
    
    # Tool lifecycle
    PRE_TOOL_USE = "PreToolUse"           # Before tool execution
    POST_TOOL_USE = "PostToolUse"         # After successful tool execution
    POST_TOOL_FAILURE = "PostToolFailure" # After tool fails
    
    # Session lifecycle
    SESSION_START = "SessionStart"        # When session begins
    SESSION_END = "SessionEnd"            # When session ends
    
    # User interaction
    USER_PROMPT_SUBMIT = "UserPromptSubmit"  # Before processing user input
    STOP = "Stop"                         # Before agent concludes response
    
    # Permission
    PERMISSION_REQUEST = "PermissionRequest"  # When permission needed
    PERMISSION_DENIED = "PermissionDenied"    # When permission denied
    
    # Subagent
    SUBAGENT_START = "SubagentStart"      # When subagent spawns
    SUBAGENT_STOP = "SubagentStop"        # When subagent completes
    
    # Compaction
    PRE_COMPACT = "PreCompact"            # Before context compaction
    POST_COMPACT = "PostCompact"          # After context compaction


class ExitCode(int, Enum):
    """Hook exit codes - semantic signals"""
    SUCCESS = 0          # Allow, continue
    BLOCK = 2            # Block the action
    WARNING = 1          # Allow but warn
    MODIFY = 3           # Allow with modified input


@dataclass
class HookContext:
    """Context passed to hooks"""
    hook_point: HookPoint
    agent_name: str
    session_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Tool-specific
    tool_name: Optional[str] = None
    tool_arguments: Optional[Dict[str, Any]] = None
    tool_result: Optional[Any] = None
    tool_error: Optional[str] = None
    
    # User-specific
    user_input: Optional[str] = None
    user_id: Optional[str] = None
    
    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'hook_point': self.hook_point.value,
            'agent_name': self.agent_name,
            'session_id': self.session_id,
            'timestamp': self.timestamp.isoformat(),
            'tool_name': self.tool_name,
            'tool_arguments': self.tool_arguments,
            'tool_result': str(self.tool_result)[:500] if self.tool_result else None,
            'tool_error': self.tool_error,
            'user_input': self.user_input,
            'user_id': self.user_id,
            'metadata': self.metadata
        }


@dataclass
class HookResult:
    """Result from hook execution"""
    exit_code: ExitCode
    message: str = ""
    modified_input: Optional[Dict[str, Any]] = None
    additional_context: Optional[str] = None
    permission_decision: Optional[str] = None  # 'allow', 'deny', 'ask'
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def should_block(self) -> bool:
        return self.exit_code == ExitCode.BLOCK
    
    @property
    def should_warn(self) -> bool:
        return self.exit_code == ExitCode.WARNING
    
    @property
    def has_modifications(self) -> bool:
        return self.modified_input is not None
    
    @property
    def is_success(self) -> bool:
        return self.exit_code == ExitCode.SUCCESS


@dataclass
class HookConfig:
    """Configuration for a hook"""
    name: str
    hook_point: HookPoint
    command: str                    # Shell command or script path
    matcher: Optional[str] = None   # Pattern to match (e.g., "Bash(git commit*)")
    enabled: bool = True
    timeout_seconds: int = 30
    once: bool = False              # Auto-remove after first execution
    priority: int = 100             # Lower = runs first
    
    # Security
    trusted: bool = False           # Skip confirmation for trusted hooks
    allow_network: bool = False     # Allow hook to make network calls
    
    def matches(self, context: HookContext) -> bool:
        """Check if hook matches the context"""
        if not self.matcher:
            return True
        
        # Parse matcher: "ToolName(pattern)" or just "pattern"
        import re
        if '(' in self.matcher:
            tool_part, pattern_part = self.matcher.split('(', 1)
            pattern_part = pattern_part.rstrip(')')
            
            if tool_part != context.tool_name:
                return False
            
            # Check pattern against arguments
            if context.tool_arguments:
                args_str = ' '.join(str(v) for v in context.tool_arguments.values())
                return bool(re.search(pattern_part, args_str))
        
        # Simple pattern match against tool name or user input
        if context.tool_name:
            return bool(re.search(self.matcher, context.tool_name))
        if context.user_input:
            return bool(re.search(self.matcher, context.user_input))
        
        return False
