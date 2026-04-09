"""Slot reservation - Optimize output token allocation"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class SlotReservation:
    """
    Claude Code's slot reservation pattern.
    Default to p99 output length, escalate on truncation.
    """
    DEFAULT_TOKENS: int = 8000   # p99 is ~5000, 8K gives buffer
    MAX_TOKENS: int = 64000      # Escalation ceiling
    
    def __init__(self, default_tokens: int = 8000, max_tokens: int = 64000):
        self.default_tokens = default_tokens
        self.max_tokens = max_tokens
        self._current_reservation = default_tokens
        self._truncation_count = 0
    
    @property
    def current(self) -> int:
        return self._current_reservation
    
    def on_truncation(self) -> int:
        """Escalate on truncation - rare (<1% of requests)"""
        self._truncation_count += 1
        self._current_reservation = min(
            self._current_reservation * 2,
            self.max_tokens
        )
        return self._current_reservation
    
    def reset(self):
        """Reset to default for new conversation"""
        self._current_reservation = self.default_tokens
        self._truncation_count = 0
    
    def get_savings_estimate(self) -> dict:
        """
        Estimate token savings vs naive 64K reservation.
        p99 output is ~5K, so we save ~59K tokens per request.
        """
        saved_per_request = self.max_tokens - self.default_tokens
        return {
            "default_reservation": self.default_tokens,
            "max_reservation": self.max_tokens,
            "tokens_saved_per_request": saved_per_request,
            "cost_savings_per_1k": f"~${saved_per_request * 0.003 / 1000:.4f}"
        }
