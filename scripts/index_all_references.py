"""Index ALL webclaw references into Chronicle — not just jurisdictions."""
import sys, re
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from agents.webclaw.core.chronicle_ledger import get_chronicle

REFERENCES_ROOT = PROJECT_ROOT / "agents" / "webclaw" / "references"
SKIP_PATTERNS = ['__pycache__', '.git', 'TX-project', 'node_modules', 'target', '.fingerprint', '.cache']

def main():
    chronicle = get_chronicle()
    
    # Purge old jurisdiction entries first
    import sqlite3
    conn = sqlite3.connect(str(PROJECT_ROOT / 'data' / 'chronicle.db'))
    conn.execute("DELETE FROM chronicle WHERE source LIKE 'jurisdiction:%'")
    conn.commit()
    purged = conn.total_changes
    conn.close()
    print(f"Purged {purged} old jurisdiction entries")
    
    files = [f for f in REFERENCES_ROOT.rglob("*.md") if not any(p in str(f) for p in SKIP_PATTERNS)]
    print(f"Indexing {len(files)} files from ALL webclaw references...")
    
    indexed = skipped = errors = 0
    total_size = 0
    
    for filepath in files:
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
            if not content.strip():
                skipped += 1
                continue
            
            total_size += len(content)
            rel = filepath.relative_to(REFERENCES_ROOT)
            parts = rel.parts
            agent = parts[0] if len(parts) > 0 else "unknown"
            
            context = f"AGENT: {agent} | PATH: {rel}\n---\n{content}"
            url = f"reference://{rel.as_posix()}"
            
            chronicle.record_fetch(
                url=url, context=context,
                source=f"reference:{agent}",
                metadata={'agent': agent, 'path': str(rel), 'size': len(content)}
            )
            indexed += 1
            if indexed % 5000 == 0:
                print(f"  Indexed: {indexed} | Size: {total_size/1024/1024:.1f}MB | Skipped: {skipped}")
        except Exception as e:
            errors += 1
            if errors <= 10:
                print(f"  Error [{filepath.name}]: {str(e)[:100]}")
    
    print(f"\n{'='*60}")
    print(f"INDEXING COMPLETE")
    print(f"  Files indexed: {indexed}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors: {errors}")
    print(f"  Total content: {total_size/1024/1024:.1f}MB")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
