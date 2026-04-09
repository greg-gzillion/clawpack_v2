"""Slot Reservation - Claude Code Pattern #9"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class SlotReservation:
    """8K default, escalate to 64K on truncation"""
    DEFAULT_TOKENS: int = 8000   # p99 output is ~5K
    MAX_TOKENS: int = 64000      # Escalation ceiling
    
    def __init__(self, default_tokens: int = 8000, max_tokens: int = 64000):
        self.default_tokens = default_tokens
        self.max_tokens = max_tokens
        self._current = default_tokens
        self._truncation_count = 0
        self._total_requests = 0
        self._tokens_saved = 0
    
    @property
    def current(self) -> int:
        return self._current
    
    def on_truncation(self) -> int:
        """Escalate on truncation (<1% of requests)"""
        self._truncation_count += 1
        self._current = min(self._current * 2, self.max_tokens)
        return self._current
    
    def on_success(self, tokens_used: int):
        """Track successful requests"""
        self._total_requests += 1
        saved = self.max_tokens - self._current
        self._tokens_saved += saved
    
    def reset(self):
        """Reset for new conversation"""
        self._current = self.default_tokens
    
    def get_stats(self) -> dict:
        """Get savings statistics"""
        return {
            "default_tokens": self.default_tokens,
            "max_tokens": self.max_tokens,
            "current": self._current,
            "truncations": self._truncation_count,
            "total_requests": self._total_requests,
            "tokens_saved": self._tokens_saved,
            "cost_saved": f"${self._tokens_saved * 0.000003:.4f}",
            "truncation_rate": f"{(self._truncation_count / max(1, self._total_requests)) * 100:.1f}%"
        }

# Global instance
_slot_reservation = SlotReservation()

def get_slot_reservation() -> SlotReservation:
    return _slot_reservation
