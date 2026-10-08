"""dataclaw shared utilities — constitutional command helpers.

Dataclaw-specific: local file indexing, Chronicle writing, data export.
"""
import json
from pathlib import Path
from datetime import datetime

DATACLAW_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = DATACLAW_DIR.parent.parent
EXPORTS = PROJECT_ROOT / "exports"

DATACLAW_REFS = DATACLAW_DIR / "references"
SKIP_DIRS = {'node_modules', 'venv', '__pycache__', '.git', 'lib64'}
SEARCH_EXTENSIONS = {'.md', '.txt', '.py', '.json', '.csv', '.yaml', '.rs', '.go', '.js', '.html'}


def search_local_files(query: str, max_results: int = 10) -> list:
    """Search the DataClaw file index (FTS5) for query matches.

    Uses agents/dataclaw/references/data_index.db. If the index is missing,
    returns an empty list (run scripts/_rebuild_data_index.py to build it).

    Return shape: [{"file": str, "match": str, "size": int}]
    """
    import sqlite3

    index_db = DATACLAW_REFS / "data_index.db"
    if not index_db.exists():
        return []

    query = query.strip()
    if not query:
        return []

    results = []
    seen_paths = set()

    try:
        conn = sqlite3.connect(str(index_db))
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        # Sanitize query for FTS5 — wrap terms in quotes for literal matching
        # but keep basic AND behavior
        terms = [t for t in query.lower().split() if len(t) > 1]
        if not terms:
            conn.close()
            return []

        # Try FTS5 first (fast path)
        try:
            fts_query = " OR ".join(f'"{t}"' for t in terms)
            c.execute("""
                SELECT fi.path, fi.filename, fi.size,
                       snippet(file_index_fts, 1, '<<', '>>', '...', 20) as snippet
                FROM file_index_fts
                JOIN file_index fi ON fi.id = file_index_fts.rowid
                WHERE file_index_fts MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (fts_query, max_results))
            for row in c.fetchall():
                path = row["path"]
                if path in seen_paths:
                    continue
                seen_paths.add(path)
                match = "content"
                snippet = row["snippet"] or ""
                if snippet:
                    match = f"snippet: {snippet[:180]}"
                results.append({
                    "file": path,
                    "match": match,
                    "size": row["size"] or 0,
                })
        except Exception:
            pass

        # Fallback: direct filename LIKE if FTS5 gave nothing
        if not results:
            like = f"%{terms[0]}%"
            c.execute("""
                SELECT path, filename, size
                FROM file_index
                WHERE LOWER(filename) LIKE ?
                LIMIT ?
            """, (like, max_results))
            for row in c.fetchall():
                path = row["path"]
                if path in seen_paths:
                    continue
                seen_paths.add(path)
                results.append({
                    "file": path,
                    "match": "filename",
                    "size": row["size"] or 0,
                })

        conn.close()
    except Exception:
        return []

    return results

def search_data_files(query: str) -> list:
    """Search JSON data files for query matches."""
    results = []
    for data_path in [PROJECT_ROOT / "data", PROJECT_ROOT / "exports"]:
        if not data_path.exists():
            continue
        for file_path in data_path.rglob("*.json"):
            if any(skip in str(file_path).lower() for skip in SKIP_DIRS):
                continue
            try:
                content = json.loads(file_path.read_text(encoding="utf-8"))
                if isinstance(content, dict):
                    for key, value in content.items():
                        if query.lower() in str(key).lower() or query.lower() in str(value).lower():
                            results.append({
                                "file": str(file_path.relative_to(PROJECT_ROOT)),
                                "key": str(key),
                                "value": str(value)[:200]
                            })
                elif isinstance(content, list):
                    for item in content[:50]:
                        if query.lower() in str(item).lower():
                            results.append({
                                "file": str(file_path.relative_to(PROJECT_ROOT)),
                                "item": str(item)[:200]
                            })
                            break
            except Exception:
                pass
            if len(results) >= 10:
                break
    return results


def index_to_chronicle(filepath: str, content_preview: str, agent=None) -> bool:
    """Index a local file discovery to Chronicle for cross-agent visibility."""
    try:
        if agent and hasattr(agent, 'record_in_chronicle'):
            agent.record_in_chronicle(
                url=f"local://{filepath}",
                context=content_preview[:500],
                source="dataclaw"
            )
            return True
    except Exception:
        pass
    return False


def count_indexed_files() -> int:
    """Count total indexable files in search paths."""
    total = 0
    search_paths = [
        DATACLAW_REFS,
        PROJECT_ROOT / "docs",
        PROJECT_ROOT / "data",
        PROJECT_ROOT / "agents" / "webclaw" / "references"
    ]
    for sp in search_paths:
        if sp.exists():
            try:
                total += sum(
                    1 for _ in sp.rglob("*")
                    if _.is_file() and not any(skip in str(_).lower() for skip in SKIP_DIRS)
                )
            except Exception:
                pass
    return total


def export_results(data_query: str, file_results: list, data_results: list, fmt: str = "json") -> str:
    """Export search results to a file. Returns filename."""
    export_data = {
        "query": data_query,
        "files": file_results,
        "data": data_results,
        "timestamp": datetime.now().isoformat()
    }
    EXPORTS.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = data_query.replace(" ", "_")[:40]

    if fmt == "json":
        fn = f"dataclaw_{name}_{ts}.json"
        (EXPORTS / fn).write_text(json.dumps(export_data, indent=2, default=str))
    elif fmt == "csv":
        import csv
        fn = f"dataclaw_{name}_{ts}.csv"
        with open(EXPORTS / fn, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["Type", "File", "Content"])
            for r in file_results:
                w.writerow(["file", r['file'], r.get('match', '')])
            for r in data_results:
                w.writerow(["data", r['file'], r.get('value', r.get('item', ''))])
    else:
        fn = f"dataclaw_{name}_{ts}.{fmt}"
        (EXPORTS / fn).write_text(str(export_data))
    return fn