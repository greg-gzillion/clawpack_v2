"""Hook types, events, and result structures - Chapter 12"""
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from pathlib import Path

class HookEvent(Enum):
    """27 hook events from Claude Code"""
    
    # Session lifecycle (2)
    SESSION_START = "session_start"
    SESSION_END = "session_end"
    
    # Tool lifecycle (5)
    PRE_TOOL_USE = "pre_tool_use"
    POST_TOOL_USE = "post_tool_use"
    POST_TOOL_USE_FAILURE = "post_tool_use_failure"
    PERMISSION_DENIED = "permission_denied"
    PERMISSION_REQUEST = "permission_request"
    
    # Stop hooks (2)
    STOP = "stop"
    SUBAGENT_STOP = "subagent_stop"
    
    # Subagent lifecycle (1)
    SUBAGENT_START = "subagent_start"
    
    # Compaction (2)
    PRE_COMPACT = "pre_compact"
    POST_COMPACT = "post_compact"
    
    # User input (1)
    USER_PROMPT_SUBMIT = "user_prompt_submit"
    
    # Configuration (4)
    CONFIG_CHANGE = "config_change"
    CWD_CHANGED = "cwd_changed"
    FILE_CHANGED = "file_changed"
    INSTRUCTIONS_LOADED = "instructions_loaded"
    
    # Task lifecycle (3)
    TASK_CREATED = "task_created"
    TASK_COMPLETED = "task_completed"
    TEAMMATE_IDLE = "teammate_idle"
    
    # Notification (3)
    NOTIFICATION = "notification"
    ELICITATION = "elicitation"
    ELICITATION_RESULT = "elicitation_result"
    
    # Setup (1)
    SETUP = "setup"
    
    @property
    def can_block(self) -> bool:
        """Whether this hook can block execution"""
        return self in [
            HookEvent.PRE_TOOL_USE,
            HookEvent.STOP,
            HookEvent.USER_PROMPT_SUBMIT,
        ]
    
    @property
    def can_modify_input(self) -> bool:
        """Whether this hook can modify input"""
        return self in [
            HookEvent.PRE_TOOL_USE,
            HookEvent.USER_PROMPT_SUBMIT,
        ]


class HookType(Enum):
    """Four hook execution types"""
    COMMAND = "command"      # Shell command
    PROMPT = "prompt"        # Single LLM call
    AGENT = "agent"          # Multi-turn agent loop
    HTTP = "http"            # Webhook


class HookExitCode(Enum):
    """Exit code semantics"""
    SUCCESS = 0
    BLOCKING_ERROR = 2
    NON_BLOCKING_WARNING = 1


@dataclass
class HookResult:
    """Result from hook execution"""
    allowed: bool = True
    block: bool = False
    modified_input: Optional[Dict] = None
    additional_context: Optional[str] = None
    reason: Optional[str] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    
    @classmethod
    def allow(cls, context: str = None) -> "HookResult":
        return cls(allowed=True, additional_context=context)
    
    @classmethod
    def deny(cls, reason: str) -> "HookResult":
        return cls(allowed=False, block=True, reason=reason)
    
    @classmethod
    def modify(cls, modified_input: Dict, context: str = None) -> "HookResult":
        return cls(allowed=True, modified_input=modified_input, additional_context=context)
    
    @classmethod
    def warn(cls, reason: str) -> "HookResult":
        return cls(allowed=True, block=False, reason=reason)


@dataclass
class HookContext:
    """Context passed to hooks"""
    event: HookEvent
    tool_name: Optional[str] = None
    tool_input: Optional[Dict] = None
    tool_use_id: Optional[str] = None
    session_id: Optional[str] = None
    agent_id: Optional[str] = None
    message: Optional[str] = None
    working_dir: Optional[Path] = None
    environment: Dict[str, str] = field(default_factory=dict)


@dataclass
class HookDefinition:
    """Hook configuration from settings.json"""
    type: HookType
    command: Optional[str] = None
    url: Optional[str] = None
    prompt: Optional[str] = None
    timeout: int = 60
    matcher: Optional[str] = None
    once: bool = False
    blocking: bool = True
    
    @classmethod
    def from_dict(cls, data: Dict) -> "HookDefinition":
        return cls(
            type=HookType(data.get("type", "command")),
            command=data.get("command"),
            url=data.get("url"),
            prompt=data.get("prompt"),
            timeout=data.get("timeout", 60),
            matcher=data.get("matcher"),
            once=data.get("once", False),
            blocking=data.get("blocking", True),
        )
