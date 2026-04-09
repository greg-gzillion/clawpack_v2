"""Cache strategies and sticky latches for prompt stability"""

from enum import Enum
from typing import Optional
from datetime import datetime

class CacheStrategy(str, Enum):
    """How a prompt section interacts with the cache"""
    STABLE = "stable"      # Never changes - maximum cache sharing
    SEMI_STABLE = "semi"   # Changes rarely - session-level cache
    VOLATILE = "volatile"  # Changes every turn - never cached

class StickyLatch:
    """
    Sticky-once latch pattern from Claude Code.
    Once set to True, never reverts for the session.
    Prevents cache-busting from mid-session toggles.
    """
    
    def __init__(self, name: str):
        self.name = name
        self._value: Optional[bool] = None
        self._set_at: Optional[datetime] = None
    
    @property
    def value(self) -> Optional[bool]:
        return self._value
    
    def set_true(self) -> bool:
        """Set to True. Returns True if this was the first time."""
        if self._value is None:
            self._value = True
            self._set_at = datetime.now()
            return True
        return False
    
    def is_set(self) -> bool:
        return self._value is True
    
    def __repr__(self) -> str:
        return f"StickyLatch({self.name}={self._value})"


# Global latches for cache-busting operations
class PromptLatches:
    """Global sticky latches that protect the prompt cache"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_latches()
        return cls._instance
    
    def _init_latches(self):
        self.cache_editing = StickyLatch("cache_editing")
        self.fast_mode = StickyLatch("fast_mode")
        self.thinking_clear = StickyLatch("thinking_clear")
        self.mcp_tools_loaded = StickyLatch("mcp_tools_loaded")
    
    def any_cache_busting_change(self) -> bool:
        """Check if any latch has been flipped this session"""
        return (self.cache_editing.is_set() or 
                self.fast_mode.is_set() or 
                self.thinking_clear.is_set())


# Singleton access
def get_latches() -> PromptLatches:
    return PromptLatches()
