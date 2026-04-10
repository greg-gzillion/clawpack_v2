"""Loop state - reconstructed at every continue"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass(frozen=True)
class LoopState:
    messages: List[Dict[str, Any]]
    turn_count: int = 0
    transition: Optional[Dict[str, Any]] = None
    
    # Recovery tracking
    max_output_tokens_recovery_count: int = 0
    has_attempted_reactive_compact: bool = False
    auto_compact_failures: int = 0
    
    # Context tracking
    token_count: int = 0
    compaction_boundary: Optional[int] = None
    
    def with_updates(self, **kwargs) -> 'LoopState':
        """Create new state with updates (immutable transition)"""
        current = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        current.update(kwargs)
        return LoopState(**current)
