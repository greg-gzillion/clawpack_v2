"""Type definitions for generator loop - Discriminated unions for all states"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, AsyncIterator
from datetime import datetime

class TerminalState(str, Enum):
    """Why the agent loop terminated"""
    COMPLETED = "completed"           # Natural completion
    STOPPED = "stopped"               # User interrupted
    MAX_TURNS = "max_turns"           # Hit turn limit
    TOKEN_LIMIT = "token_limit"       # Context window full
    ERROR = "error"                   # Unrecoverable error
    TIMEOUT = "timeout"               # Operation timeout
    CANCELLED = "cancelled"           # Explicit cancellation


class LoopState(str, Enum):
    """Current state of the agent loop"""
    IDLE = "idle"                      # Not running
    STREAMING = "streaming"            # Receiving model output
    EXECUTING_TOOLS = "executing_tools" # Running tool calls
    WAITING_PERMISSION = "waiting_permission"  # User approval needed
    COMPACTING = "compacting"          # Compressing context
    ERROR = "error"                    # Error state


@dataclass
class TurnResult:
    """Result of a single turn in the conversation"""
    turn_number: int
    user_input: Optional[str] = None
    assistant_output: Optional[str] = None
    tool_calls: List[Dict] = field(default_factory=list)
    tool_results: List[Dict] = field(default_factory=list)
    tokens_used: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'turn': self.turn_number,
            'input': self.user_input,
            'output': self.assistant_output,
            'tool_calls': len(self.tool_calls),
            'tokens': self.tokens_used,
            'timestamp': self.timestamp.isoformat()
        }


@dataclass
class LoopResult:
    """Final result from the agent loop"""
    terminal_state: TerminalState
    turns: List[TurnResult]
    total_tokens: int
    total_tool_calls: int
    duration_ms: float
    error: Optional[str] = None
    
    def was_successful(self) -> bool:
        return self.terminal_state == TerminalState.COMPLETED


@dataclass
class StreamChunk:
    """A chunk of streaming output"""
    type: str  # 'text', 'tool_call', 'thinking', 'error'
    content: str
    tool_name: Optional[str] = None
    tool_id: Optional[str] = None
    is_final: bool = False
