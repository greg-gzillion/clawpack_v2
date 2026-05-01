"""Immutable audit trail — append-only, hash-chained log."""
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

from .types import AUDIT_LOG_DIR


class AuditTrail:
    """Append-only, hash-chained audit log. Immutable by design."""
    
    def __init__(self, base_dir: Path):
        self.audit_dir = base_dir / AUDIT_LOG_DIR
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        self._chain_file = self.audit_dir / "CHAIN.json"
        self._ensure_chain()
    
    def _ensure_chain(self):
        if not self._chain_file.exists():
            self._chain_file.write_text(json.dumps({
                "genesis": hashlib.sha256(b"CLAWPACK_AUDIT_GENESIS").hexdigest(),
                "entries": []
            }, indent=2))
    
    def _read_chain(self) -> dict:
        return json.loads(self._chain_file.read_text())
    
    def _write_chain(self, chain: dict):
        self._chain_file.write_text(json.dumps(chain, indent=2))
    
    def append(self, event_type: str, data: dict) -> str:
        """Append immutable entry to audit chain. Returns entry hash."""
        chain = self._read_chain()
        previous_hash = chain["entries"][-1]["hash"] if chain["entries"] else chain["genesis"]
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "previous_hash": previous_hash,
            "data": data,
        }
        entry["hash"] = hashlib.sha256(
            json.dumps(entry, sort_keys=True).encode()
        ).hexdigest()
        chain["entries"].append(entry)
        self._write_chain(chain)
        log_file = self.audit_dir / f"event_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
        log_file.write_text(json.dumps(entry, indent=2))
        return entry["hash"]
    
    def verify_integrity(self) -> bool:
        """Verify entire chain has not been tampered with."""
        chain = self._read_chain()
        expected = chain["genesis"]
        for entry in chain["entries"]:
            if entry["previous_hash"] != expected:
                return False
            recalc = hashlib.sha256(
                json.dumps({k: v for k, v in entry.items() if k != "hash"}, sort_keys=True).encode()
            ).hexdigest()
            if recalc != entry["hash"]:
                return False
            expected = entry["hash"]
        return True


__all__ = ['AuditTrail']