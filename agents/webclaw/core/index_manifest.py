"""WebClaw Index Manifest — file fingerprint tracker for incremental indexing.

   Prevents duplicate indexing. Tracks every reference file by hash.
   Only re-indexes files that have changed since last ingest.
"""
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REFERENCES_DIR = PROJECT_ROOT / "agents" / "webclaw" / "references"
MANIFEST_PATH = PROJECT_ROOT / "data" / "index_manifest.json"


class IndexManifest:
    """Tracks every reference file by hash. Enables safe incremental indexing."""

    def __init__(self):
        self.manifest: Dict[str, Dict] = {}
        self._load()

    def _load(self):
        if MANIFEST_PATH.exists():
            try:
                self.manifest = json.loads(MANIFEST_PATH.read_text())
            except (json.JSONDecodeError, KeyError):
                self.manifest = {}

    def _save(self):
        MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST_PATH.write_text(json.dumps(self.manifest, indent=2))

    def hash_file(self, path: Path) -> str:
        """SHA256 hash of file contents."""
        return hashlib.sha256(path.read_bytes()).hexdigest()[:16]

    def needs_indexing(self, path: Path) -> bool:
        """Check if a file needs to be indexed (new or changed)."""
        key = str(path.relative_to(PROJECT_ROOT))
        current_hash = self.hash_file(path)

        if key not in self.manifest:
            return True  # New file

        if self.manifest[key].get("hash") != current_hash:
            return True  # Changed file

        return False  # Unchanged

    def mark_indexed(self, path: Path):
        """Mark a file as successfully indexed."""
        key = str(path.relative_to(PROJECT_ROOT))
        self.manifest[key] = {
            "hash": self.hash_file(path),
            "size": path.stat().st_size,
            "indexed_at": datetime.now(timezone.utc).isoformat(),
            "path": key,
        }
        self._save()

    def get_unindexed_files(self) -> list:
        """Return list of files that need indexing."""
        unindexed = []
        for md_file in REFERENCES_DIR.rglob("*.md"):
            if self.needs_indexing(md_file):
                unindexed.append(md_file)
        return unindexed

    def get_stats(self) -> Dict:
        """Get manifest statistics."""
        indexed = len(self.manifest)
        total_files = len(list(REFERENCES_DIR.rglob("*.md")))
        return {
            "total_files": total_files,
            "indexed": indexed,
            "unindexed": total_files - indexed,
            "manifest_path": str(MANIFEST_PATH),
        }


__all__ = ["IndexManifest"]