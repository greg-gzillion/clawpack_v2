"""Chronicle Auditor — immutable audit trail for every model interaction."""

import json
import hashlib
from pathlib import Path
from typing import Dict, Any

from .config import CHRONICLE_PATH
from .response import LLMResponse


class ChronicleAuditor:
    """Immutable audit trail for every model interaction"""
    
    def __init__(self):
        self.ledger_path = CHRONICLE_PATH
        self._ensure_ledger()
    
    def _ensure_ledger(self):
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.ledger_path.exists():
            self.ledger_path.write_text(json.dumps({
                "genesis": hashlib.sha256(b"CLAWPACK_CHRONICLE_GENESIS").hexdigest(),
                "entries": []
            }, indent=2))
    
    def log(self, agent: str, prompt: str, response: LLMResponse):
        entry = {
            "timestamp": response.timestamp,
            "agent": agent,
            "model": response.model,
            "provider": response.provider.value,
            "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest()[:16],
            "response_hash": hashlib.sha256(response.content.encode()).hexdigest()[:16],
            "tokens_used": response.tokens_used,
            "cost": response.cost,
            "duration_ms": response.duration_ms,
            "cached": response.cached,
            "decision": response.access_decision.value,
            "fallback_used": response.fallback_used,
            "fallback_provider": response.fallback_provider,
        }
        try:
            if self.ledger_path.exists():
                ledger_data = json.loads(self.ledger_path.read_text())
                if isinstance(ledger_data, list):
                    ledger_data.append(entry)
                elif isinstance(ledger_data, dict):
                    ledger_data.setdefault("entries", []).append(entry)
            else:
                ledger_data = [entry]
            self.ledger_path.write_text(json.dumps(ledger_data, indent=2))
        except Exception as e:
            print(f"Chronicle audit failed: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        if not self.ledger_path.exists():
            return {"total_interactions": 0, "by_agent": {}, "by_model": {}, "total_cost": 0.0}
        try:
            ledger_data = json.loads(self.ledger_path.read_text())
            if isinstance(ledger_data, list):
                entries = ledger_data
            elif isinstance(ledger_data, dict):
                entries = ledger_data.get("entries", [])
            else:
                entries = []
        except (json.JSONDecodeError, KeyError):
            return {"total_interactions": 0, "by_agent": {}, "by_model": {}, "total_cost": 0.0}
        stats = {
            "total_interactions": len(entries),
            "by_agent": {}, "by_model": {}, "by_provider": {},
            "total_cost": 0.0, "total_tokens": 0, "avg_latency_ms": 0.0,
            "recent_entries": entries[-10:] if entries else [],
        }
        for entry in entries:
            agent = entry.get("agent", "unknown")
            model = entry.get("model", "unknown")
            provider = entry.get("provider", "unknown")
            stats["by_agent"][agent] = stats["by_agent"].get(agent, 0) + 1
            stats["by_model"][model] = stats["by_model"].get(model, 0) + 1
            stats["by_provider"][provider] = stats["by_provider"].get(provider, 0) + 1
            stats["total_cost"] += entry.get("cost", 0)
            stats["total_tokens"] += entry.get("tokens_used", 0)
        if entries:
            stats["avg_latency_ms"] = sum(e.get("duration_ms", 0) for e in entries) / len(entries)
        return stats


__all__ = ['ChronicleAuditor']
