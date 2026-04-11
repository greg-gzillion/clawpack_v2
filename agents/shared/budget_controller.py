"""Adaptive budget controller for token management - inspired by Continuity Ledger"""

from dataclasses import dataclass
from typing import Dict, List
from enum import Enum
import json
from pathlib import Path

class BudgetAction(Enum):
    ADMIT = "admit"
    COMPRESS = "compress"
    ESCALATE = "escalate"
    REACTIVATE = "reactivate"

@dataclass
class BudgetState:
    current_tokens: int
    max_tokens: int
    compression_count: int
    escalation_count: int
    success_rate: float

class AdaptiveBudgetController:
    """Bounded adaptive controller for context budget"""
    
    def __init__(self, max_tokens: int = 200000):
        self.max_tokens = max_tokens
        self.thresholds = {
            'compress': 0.70,   # 70% - start compressing
            'escalate': 0.90,   # 90% - escalate to larger model
            'critical': 0.95    # 95% - emergency compression
        }
        self.history: List[BudgetState] = []
        self.storage_path = Path.home() / ".clawpack/budget"
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def decide_action(self, current_tokens: int, success_rate: float) -> BudgetAction:
        """Decide what action to take based on current budget"""
        ratio = current_tokens / self.max_tokens
        
        # Learn from history
        self.history.append(BudgetState(current_tokens, self.max_tokens, 0, 0, success_rate))
        
        if ratio >= self.thresholds['critical']:
            return BudgetAction.ESCALATE
        elif ratio >= self.thresholds['escalate']:
            return BudgetAction.COMPRESS
        elif ratio >= self.thresholds['compress'] and success_rate < 0.7:
            return BudgetAction.COMPRESS
        else:
            return BudgetAction.ADMIT
    
    def compress_context(self, context: str, target_ratio: float = 0.5) -> str:
        """Intelligently compress context"""
        lines = context.split('\n')
        if len(lines) < 10:
            return context
        
        # Keep first and last parts
        keep_start = int(len(lines) * target_ratio / 2)
        keep_end = int(len(lines) * target_ratio / 2)
        
        compressed = lines[:keep_start]
        compressed.append(f"... [Compressed {len(lines) - keep_start - keep_end} lines] ...")
        compressed.extend(lines[-keep_end:])
        
        return '\n'.join(compressed)
    
    def get_stats(self) -> Dict:
        """Get controller statistics"""
        return {
            'max_tokens': self.max_tokens,
            'thresholds': self.thresholds,
            'history_length': len(self.history),
            'avg_success_rate': sum(h.success_rate for h in self.history[-10:]) / 10 if self.history else 0
        }

budget_controller = AdaptiveBudgetController()
