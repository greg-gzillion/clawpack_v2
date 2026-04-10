"""Terminal states - exactly why the loop stopped"""
from enum import Enum
from typing import Optional
from dataclasses import dataclass

class TerminalReason(Enum):
    COMPLETED = "completed"
    USER_ABORT = "user_abort"
    MAX_TURNS = "max_turns"
    TOKEN_BUDGET = "token_budget"
    PROMPT_TOO_LONG = "prompt_too_long"
    MODEL_ERROR = "model_error"
    STOP_HOOK = "stop_hook"
    PERMISSION_DENIED = "permission_denied"

@dataclass
class Terminal:
    reason: TerminalReason
    message: Optional[str] = None
    turn_count: int = 0
