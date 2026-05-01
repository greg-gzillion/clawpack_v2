"""Constitutional Decision Ledger — Immutable record of every governed decision.

   Every agent action that passes through the three pillars creates a record.
   This is the Constitutional Court Record of Clawpack V2.
   
   Without this: you cannot audit failures.
   With this: every decision is traceable, replayable, and contestable.
"""
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER_PATH = PROJECT_ROOT / "data" / "constitutional_ledger.json"


class DecisionLedger:
    """Append-only ledger of constitutional decisions. Immutable by design."""

    def __init__(self):
        self.ledger_path = LEDGER_PATH
        self._ensure_ledger()

    def _ensure_ledger(self):
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.ledger_path.exists():
            self.ledger_path.write_text(json.dumps({
                "genesis": hashlib.sha256(b"CLAWPACK_CONSTITUTIONAL_GENESIS").hexdigest(),
                "entries": [],
                "version": "v1.0",
            }, indent=2))

    def record(self, agent: str, query: str, decision: Dict[str, Any]) -> str:
        """Record a constitutional decision. Returns entry hash."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent": agent,
            "query": query[:500],
            "resolved_source": decision.get("source", "unknown"),
            "source_type": decision.get("source_type", "inference"),
            "confidence": decision.get("confidence", 0),
            "conflicts": len(decision.get("conflicts", [])),
            "policy_checks": decision.get("policy_checks", []),
            "status": decision.get("status", "unknown"),
        }
        entry["hash"] = hashlib.sha256(
            json.dumps(entry, sort_keys=True).encode()
        ).hexdigest()[:16]

        ledger = json.loads(self.ledger_path.read_text())
        ledger["entries"].append(entry)
        self.ledger_path.write_text(json.dumps(ledger, indent=2))
        return entry["hash"]

    def record_action(self, agent: str, action: str, policy_result: Dict,
                      context: Dict = None) -> str:
        """Record an action subject to execution policy."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent": agent,
            "action": action,
            "allowed": policy_result.get("allowed", False),
            "level": str(policy_result.get("level", "unknown")),
            "reason": policy_result.get("reason", ""),
            "context": context or {},
        }
        entry["hash"] = hashlib.sha256(
            json.dumps(entry, sort_keys=True).encode()
        ).hexdigest()[:16]

        ledger = json.loads(self.ledger_path.read_text())
        ledger["entries"].append(entry)
        self.ledger_path.write_text(json.dumps(ledger, indent=2))
        return entry["hash"]

    def get_stats(self) -> Dict:
        """Get constitutional statistics."""
        if not self.ledger_path.exists():
            return {"entries": 0}
        ledger = json.loads(self.ledger_path.read_text())
        entries = ledger.get("entries", [])
        
        stats = {
            "total_decisions": len(entries),
            "by_agent": {},
            "by_source_type": {},
            "conflicts_detected": 0,
            "actions_blocked": 0,
            "avg_confidence": 0,
        }
        
        for e in entries:
            agent = e.get("agent", "unknown")
            stats["by_agent"][agent] = stats["by_agent"].get(agent, 0) + 1
            
            st = e.get("source_type", "")
            if st:
                stats["by_source_type"][st] = stats["by_source_type"].get(st, 0) + 1
            
            if e.get("conflicts", 0) > 0:
                stats["conflicts_detected"] += 1
            
            if not e.get("allowed", True):
                stats["actions_blocked"] += 1
            
            if e.get("confidence"):
                stats["avg_confidence"] += e["confidence"]
        
        if stats["total_decisions"] > 0:
            stats["avg_confidence"] = round(
                stats["avg_confidence"] / stats["total_decisions"], 4
            )
        
        return stats

    def recent_decisions(self, limit: int = 20) -> List[Dict]:
        """Get recent constitutional decisions."""
        if not self.ledger_path.exists():
            return []
        ledger = json.loads(self.ledger_path.read_text())
        return ledger.get("entries", [])[-limit:]


_ledger: Optional[DecisionLedger] = None

def get_ledger() -> DecisionLedger:
    global _ledger
    if _ledger is None:
        _ledger = DecisionLedger()
    return _ledger


__all__ = ["DecisionLedger", "get_ledger"]