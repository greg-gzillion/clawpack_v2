"""
Rebuild the DataClaw local file search index.

Walks the corpus under agents/webclaw/references/, docs/, data/, exports/,
and populates agents/dataclaw/references/data_index.db with a file_index
table + FTS5 virtual table.

Schema:
    file_index:
        id (INTEGER PRIMARY KEY)
        path (TEXT, unique)         # relative to project root
        filename (TEXT)             # basename
        agent (TEXT)                # inferred from path (lawclaw, mediclaw, ...)
        size (INTEGER)
        mtime (REAL)
        preview (TEXT)              # first 500 chars of content

    file_index_fts (FTS5):
        filename, preview
        content='file_index', content_rowid='id'

This script writes ONLY to agents/dataclaw/references/data_index.db.
It does NOT touch runtime/chronicle.db.
"""
import sqlite3
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INDEX_DB = PROJECT_ROOT / "agents" / "dataclaw" / "references" / "data_index.db"

SEARCH_PATHS = [
    PROJECT_ROOT / "agents" / "webclaw" / "references",
    PROJECT_ROOT / "agents" / "dataclaw" / "references",
    PROJECT_ROOT / "docs",
    PROJECT_ROOT / "data",
    PROJECT_ROOT / "exports",
]

SKIP_DIRS = {"node_modules", "venv", "__pycache__", ".git", "lib64", ".mypy_cache"}

SEARCH_EXTENSIONS = {
    ".md", ".txt", ".py", ".json", ".csv", ".yaml", ".yml",
    ".rs", ".go", ".js", ".ts", ".html", ".xml", ".toml", ".ini", ".cfg",
}

KNOWN_AGENTS = {
    "lawclaw", "claw_coder", "crustyclaw", "mediclaw", "designclaw",
    "draftclaw", "dreamclaw", "interpretclaw", "langclaw", "liberateclaw",
    "dataclaw", "drawclaw", "flowclaw", "docuclaw", "llmclaw",
    "mathematicaclaw", "plotclaw", "rustypycraw", "txclaw", "webclaw", "fileclaw",
}


def infer_agent(rel_path: str) -> str:
    """Infer which agent owns a file based on its path."""
    parts = rel_path.replace("\\", "/").split("/")
    for part in parts:
        if part in KNOWN_AGENTS:
            return part
    return ""


def read_preview(path: Path, max_chars: int = 500) -> str:
    """Read up to max_chars from a file, handling encoding errors."""
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
        return content[:max_chars]
    except Exception:
        return ""


def main():
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Index DB: {INDEX_DB}")
    print()

    # Backup existing
    if INDEX_DB.exists():
        backup = INDEX_DB.with_suffix(".db.bak-pre-rebuild")
        import shutil
        shutil.copy2(INDEX_DB, backup)
        print(f"Backed up old index to {backup.name}")

    # Fresh DB
    if INDEX_DB.exists():
        INDEX_DB.unlink()

    INDEX_DB.parent.mkdir(parents=True, exist_ok=True)

    db = sqlite3.connect(str(INDEX_DB))
    c = db.cursor()

    # Create schema
    c.execute("""
        CREATE TABLE file_index (
            id INTEGER PRIMARY KEY,
            path TEXT NOT NULL UNIQUE,
            filename TEXT NOT NULL,
            agent TEXT,
            size INTEGER,
            mtime REAL,
            preview TEXT
        )
    """)
    c.execute("""
        CREATE VIRTUAL TABLE file_index_fts USING fts5(
            filename, preview,
            content='file_index',
            content_rowid='id'
        )
    """)
    # Triggers to keep FTS in sync
    c.execute("""
        CREATE TRIGGER file_index_ai AFTER INSERT ON file_index BEGIN
            INSERT INTO file_index_fts(rowid, filename, preview)
            VALUES (new.id, new.filename, new.preview);
        END
    """)
    c.execute("""
        CREATE TRIGGER file_index_ad AFTER DELETE ON file_index BEGIN
            INSERT INTO file_index_fts(file_index_fts, rowid, filename, preview)
            VALUES ('delete', old.id, old.filename, old.preview);
        END
    """)
    db.commit()

    print("Schema created.")
    print()

    # Walk and index
    start = time.time()
    count = 0
    skipped = 0

    for root in SEARCH_PATHS:
        if not root.exists():
            print(f"  [skip] {root} (not found)")
            continue
        print(f"  Scanning {root.relative_to(PROJECT_ROOT)}...")
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            # Skip rules
            path_str = str(path).lower()
            if any(skip in path_str for skip in SKIP_DIRS):
                skipped += 1
                continue
            if path.suffix not in SEARCH_EXTENSIONS:
                skipped += 1
                continue

            try:
                rel = str(path.relative_to(PROJECT_ROOT))
                stat = path.stat()
                preview = read_preview(path)
                agent = infer_agent(rel)

                c.execute("""
                    INSERT OR IGNORE INTO file_index
                    (path, filename, agent, size, mtime, preview)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (rel, path.name, agent, stat.st_size, stat.st_mtime, preview))
                count += 1

                if count % 5000 == 0:
                    db.commit()
                    elapsed = time.time() - start
                    print(f"    ... {count} indexed ({elapsed:.0f}s)")
            except Exception as e:
                print(f"    [error] {rel}: {e}")
                continue

    db.commit()

    # Verify
    c.execute("SELECT COUNT(*) FROM file_index")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM file_index_fts")
    fts_total = c.fetchone()[0]

    db.close()

    elapsed = time.time() - start
    size_mb = INDEX_DB.stat().st_size / 1024 / 1024

    print()
    print("=" * 60)
    print(f"Index rebuild complete")
    print(f"  Files indexed: {total}")
    print(f"  FTS entries:   {fts_total}")
    print(f"  Skipped:       {skipped}")
    print(f"  DB size:       {size_mb:.1f} MB")
    print(f"  Time:          {elapsed:.1f}s")
    print("=" * 60)


if __name__ == "__main__":
    main()