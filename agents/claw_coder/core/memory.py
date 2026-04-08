"""Shared memory integration for cross-agent learning"""

import sqlite3
from pathlib import Path
from datetime import datetime

class SharedMemory:
    def __init__(self):
        self.db_path = Path.home() / ".claw_memory" / "shared_memory.db"
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS code_knowledge (
                    id INTEGER PRIMARY KEY,
                    language TEXT,
                    pattern TEXT,
                    code TEXT,
                    description TEXT,
                    source_agent TEXT,
                    timestamp TEXT,
                    usage_count INTEGER DEFAULT 1
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_language ON code_knowledge(language)
            """)
    
    def save_pattern(self, language: str, pattern: str, code: str, description: str = ""):
        """Save a code pattern to shared memory"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO code_knowledge 
                (language, pattern, code, description, source_agent, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (language, pattern, code, description, "claw_coder", datetime.now().isoformat()))
    
    def search_patterns(self, language: str, query: str, limit: int = 5):
        """Search for code patterns"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT pattern, code, description FROM code_knowledge
                WHERE language = ? AND (pattern LIKE ? OR description LIKE ?)
                LIMIT ?
            """, (language, f"%{query}%", f"%{query}%", limit))
            return cursor.fetchall()
