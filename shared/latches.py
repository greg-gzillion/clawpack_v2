"""Sticky Latches - Claude Code Pattern #8"""

from datetime import datetime
from typing import Optional

class StickyLatch:
    """Once set to True, never reverts for the session"""
    
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
        return (self.cache_editing.is_set() or 
                self.fast_mode.is_set() or 
                self.thinking_clear.is_set())

def get_latches() -> PromptLatches:
    return PromptLatches()
