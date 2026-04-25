"""ONE-TIME: Extract all URLs from webclaw/ and load into chronicle ledger."""
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(r"C:\Users\greg\dev\clawpack_v2")
WEBCLAW_DIR = PROJECT_ROOT / "agents" / "webclaw"

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(WEBCLAW_DIR / "core"))

from chronicle_ledger import get_chronicle

EXCLUDE = {"node_modules", ".next", "target", "venv", "__pycache__", ".git",
           "dist", "build", ".turbo", "coverage", "debug", "incremental",
           ".fingerprint", "incremental"}
SKIP_EXT = {".lock", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
            ".woff", ".woff2", ".ttf", ".eot", ".mp4", ".mp3", ".webm", ".map",
            ".exe", ".dll", ".so", ".o", ".bin", ".wasm", ".rlib", ".rmeta"}

URL_RE = re.compile(r"https?://[^\s<>\"'{}|\\^\[\]]+")

def extract_and_index():
    chronicle = get_chronicle()
    existing = {c.url for c in chronicle.cards}
    urls = set()
    files_scanned = 0
    new_count = 0

    for fp in WEBCLAW_DIR.rglob("*"):
        # Skip excluded dirs BEFORE touching filesystem
        parts = set(fp.parts)
        if EXCLUDE & parts:
            continue
        if fp.is_file():
            if fp.suffix.lower() in SKIP_EXT:
                continue
            try:
                content = fp.read_text(encoding="utf-8", errors="ignore")
                found = URL_RE.findall(content)
                for u in found:
                    u = u.rstrip(".,;:!?)}]\"'")
                    if u and u not in existing and u not in urls:
                        urls.add(u)
                        new_count += 1
                files_scanned += 1
                if files_scanned % 1000 == 0:
                    print(f"  {files_scanned} files... {new_count} new URLs")
            except:
                pass

    print(f"\nScanned {files_scanned} files. {new_count} new URLs to index.")

    for i, url in enumerate(sorted(urls)):
        chronicle.record_fetch(
            url=url,
            context="Indexed from webclaw references",
            source="webclaw_indexer"
        )
        if (i + 1) % 500 == 0:
            print(f"  Indexed {i + 1}/{new_count}...")

    stats = chronicle.get_stats()
    print(f"\nDONE. Chronicle now has {stats['total_cards']} cards, {stats['unique_urls']} unique URLs.")
    print(f"Ledger saved to: {chronicle.ledger_path}")

if __name__ == "__main__":
    print("Extracting URLs from agents/webclaw/ ...")
    print("Excluding: node_modules, .next, target, venv, build artifacts\n")
    extract_and_index()
