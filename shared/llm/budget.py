"""Budget Controller — enforces spending limits per agent."""

import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime, timezone

from .config import BUDGET_PATH
from .response import AccessDecision


class BudgetController:
    """Enforces spending limits per agent with daily caps"""
    
    def __init__(self):
        self.daily_budget: float = 50.0
        self.agent_budgets: Dict[str, float] = {
            "claw_coder": 15.0, "lawclaw": 10.0, "mediclaw": 10.0,
            "txclaw": 10.0, "webclaw": 5.0, "llmclaw": 25.0,
            "default": 5.0,
        }
        self._daily_usage: Dict[str, float] = {}
        self._load_state()
    
    def _load_state(self):
        if BUDGET_PATH.exists():
            try:
                data = json.loads(BUDGET_PATH.read_text())
                self._daily_usage = data.get("usage", {})
                self.daily_budget = data.get("global_budget", 50.0)
                self.agent_budgets.update(data.get("agent_budgets", {}))
            except (json.JSONDecodeError, KeyError):
                pass
    
    def _save_state(self):
        BUDGET_PATH.write_text(json.dumps({
            "usage": self._daily_usage,
            "global_budget": self.daily_budget,
            "agent_budgets": self.agent_budgets,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }, indent=2))
    
    def check(self, agent: str, estimated_cost: float = 0.001) -> AccessDecision:
        agent_budget = self.agent_budgets.get(agent, self.agent_budgets["default"])
        used = self._daily_usage.get(agent, 0.0)
        total_used = sum(self._daily_usage.values())
        if total_used + estimated_cost > self.daily_budget:
            return AccessDecision.DENIED_BUDGET
        if used + estimated_cost > agent_budget:
            return AccessDecision.DENIED_BUDGET
        return AccessDecision.ALLOWED
    
    def record(self, agent: str, cost: float):
        self._daily_usage[agent] = self._daily_usage.get(agent, 0.0) + cost
        self._save_state()
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "daily_budget": self.daily_budget,
            "total_used": sum(self._daily_usage.values()),
            "remaining": self.daily_budget - sum(self._daily_usage.values()),
            "by_agent": dict(self._daily_usage),
            "agent_limits": dict(self.agent_budgets),
        }


__all__ = ['BudgetController']
