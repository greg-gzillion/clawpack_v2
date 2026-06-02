"""Chronicle Ledger - SQLite-backed with FTS5 full-text search"""
import sqlite3, hashlib, json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class ChronicleLedger:
    def __init__(self, db_path=None):
        self.db_path = db_path or Path(__file__).parent.parent.parent.parent / "runtime" / "chronicle.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute('PRAGMA journal_mode=WAL')
            conn.execute('PRAGMA synchronous=NORMAL')
            conn.execute('''CREATE TABLE IF NOT EXISTS chronicle (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL, context TEXT NOT NULL, source TEXT NOT NULL,
                timestamp TEXT NOT NULL, recovery_key TEXT UNIQUE, metadata TEXT DEFAULT '{}'
            )''')
            conn.execute('''CREATE VIRTUAL TABLE IF NOT EXISTS chronicle_fts USING fts5(
                url, context, source, content=chronicle, content_rowid=id
            )''')
            conn.execute('''CREATE TRIGGER IF NOT EXISTS chronicle_ai AFTER INSERT ON chronicle BEGIN
                INSERT INTO chronicle_fts(rowid, url, context, source) VALUES (new.id, new.url, new.context, new.source);
            END''')
            conn.commit()

    def record_fetch(self, url, context, source, metadata=None):
        rk = hashlib.sha256(f'{url}{context}{source}'.encode()).hexdigest()
        meta = json.dumps(metadata or {})
        with sqlite3.connect(str(self.db_path)) as conn:
            try:
                c = conn.execute('INSERT OR IGNORE INTO chronicle (url,context,source,timestamp,recovery_key,metadata) VALUES (?,?,?,?,?,?)',
                    (url, context, source, datetime.utcnow().isoformat(), rk, meta))
                conn.commit()
                return c.lastrowid
            except: return 0

    def recover_by_context(self, query: str, limit: int = 5, source_filter: str = None) -> List[Dict]:
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            # Try FTS first with source filter
            rows = []
            try:
                if source_filter:
                    rows = conn.execute("""
                        SELECT c.* FROM chronicle c
                        JOIN chronicle_fts f ON c.id = f.rowid
                        WHERE chronicle_fts MATCH ? AND c.source LIKE ?
                        ORDER BY rank
                        LIMIT ?
                    """, (query, f"%{source_filter}%", limit)).fetchall()
                else:
                    rows = conn.execute("""
                        SELECT c.* FROM chronicle c
                        JOIN chronicle_fts f ON c.id = f.rowid
                        WHERE chronicle_fts MATCH ?
                        ORDER BY rank
                        LIMIT ?
                    """, (query, limit)).fetchall()
                if rows:
                    return [dict(r) for r in rows]
            except:
                pass
            # If FTS5 returned empty, extract keywords and retry
            if not rows:
                keywords = ' OR '.join([w for w in re.findall(r'[a-zA-Z0-9]{3,}', query)
                    if w.lower() not in ('the','and','for','what','where','when','who','how','why','are','was','did','does','has','had','can','will','is','court','county','city','state','municipal')])
                if keywords:
                    try:
                        if source_filter:
                            rows = conn.execute(
                                """SELECT c.* FROM chronicle c JOIN chronicle_fts f ON c.id = f.rowid WHERE chronicle_fts MATCH ? AND c.source LIKE ? ORDER BY rank LIMIT ?""",
                                (keywords, f"%{source_filter}%", limit)).fetchall()
                        else:
                            rows = conn.execute(
                                """SELECT c.* FROM chronicle c JOIN chronicle_fts f ON c.id = f.rowid WHERE chronicle_fts MATCH ? ORDER BY rank LIMIT ?""",
                                (keywords, limit)).fetchall()
                        if rows:
                            return [dict(r) for r in rows]
                    except:
                        pass
            # Fallback LIKE search with source filter
            like = f"%{query}%"
            if source_filter:
                rows = conn.execute("""
                    SELECT * FROM chronicle
                    WHERE (context LIKE ? OR url LIKE ? OR source LIKE ?)
                    AND source LIKE ?
                    ORDER BY id DESC
                    LIMIT ?
                """, (like, like, like, f"%{source_filter}%", limit)).fetchall()
            else:
                rows = conn.execute("""
                    SELECT * FROM chronicle
                    WHERE context LIKE ? OR url LIKE ? OR source LIKE ?
                    ORDER BY id DESC
                    LIMIT ?
                """, (like, like, like, limit)).fetchall()
            return [dict(r) for r in rows]

_chronicle = None
def get_chronicle():
    global _chronicle
    if _chronicle is None: _chronicle = ChronicleLedger()
    return _chronicle