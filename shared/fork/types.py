"""Fork agent type definitions"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime


class ForkStatus(str, Enum):
    """Status of a forked agent"""
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


@dataclass
class ForkConfig:
    """Configuration for a forked agent"""
    max_turns: int = 25
    max_tokens: int = 50000
    timeout_seconds: int = 300
    inherit_tools: bool = True
    inherit_memory: bool = True
    allowed_tools: List[str] = field(default_factory=list)
    blocked_tools: List[str] = field(default_factory=list)
    system_prompt: Optional[str] = None


@dataclass
class ForkContext:
    """Context passed to a forked agent"""
    task: str
    parent_session_id: str
    fork_id: str
    created_at: datetime = field(default_factory=datetime.now)
    variables: Dict[str, Any] = field(default_factory=dict)
    
    def to_system_prompt(self) -> str:
        """Generate system prompt for forked agent"""
        return f"""You are a specialized sub-agent forked from the main Clawpack agent.
Your task: {self.task}

Guidelines:
- Focus ONLY on the assigned task
- Return a concise, actionable result
- Do not engage in general conversation
- Use tools only when necessary
- Complete in {self.variables.get('max_turns', 25)} turns or less

Parent session: {self.parent_session_id}
Fork ID: {self.fork_id}
"""


@dataclass
class ForkResult:
    """Result from a forked agent"""
    fork_id: str
    status: ForkStatus
    result: Optional[str] = None
    error: Optional[str] = None
    turns_used: int = 0
    tokens_used: int = 0
    cache_hit: bool = False
    cache_savings_tokens: int = 0
    duration_ms: float = 0
    tool_calls: List[Dict] = field(default_factory=list)
    
    @property
    def success(self) -> bool:
        return self.status == ForkStatus.COMPLETED
    
    def to_summary(self) -> str:
        """Human-readable summary"""
        if self.success:
            return f"✅ Fork {self.fork_id}: {self.result[:100]}... ({self.turns_used} turns, {self.tokens_used} tokens)"
        else:
            return f"❌ Fork {self.fork_id}: {self.error}"
