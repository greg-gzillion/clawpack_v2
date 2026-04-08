"""Shared memory for cross-agent learning"""

import sqlite3
from pathlib import Path
from datetime import datetime

SHARED_DB = Path.home() / ".claw_memory" / "shared_memory.db"

class SharedMemory:
    def __init__(self, agent_name="webclaw"):
        self.agent_name = agent_name
        self.table_name = f"{agent_name}_knowledge"
        self._init_table()
    
    def _init_table(self):
        SHARED_DB.parent.mkdir(exist_ok=True)
        conn = sqlite3.connect(str(SHARED_DB))
        conn.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY,
                query TEXT UNIQUE,
                response TEXT,
                category TEXT,
                source_agent TEXT,
                timestamp TEXT,
                usage_count INTEGER DEFAULT 1
            )
        ''')
        conn.commit()
        conn.close()
    
    def save(self, query, response, category="web_research"):
        """Save to shared memory"""
        conn = sqlite3.connect(str(SHARED_DB))
        conn.execute(f'''
            INSERT OR REPLACE INTO {self.table_name}
            (query, response, category, source_agent, timestamp, usage_count)
            VALUES (?, ?, ?, ?, ?, COALESCE((SELECT usage_count + 1 FROM {self.table_name} WHERE query = ?), 1))
        ''', (query, response, category, self.agent_name, datetime.now().isoformat(), query))
        conn.commit()
        conn.close()
        print(f"💾 Saved to shared memory: {query[:50]}...")
    
    def recall(self, query, max_results=5):
        """Recall from this agent's memory"""
        conn = sqlite3.connect(str(SHARED_DB))
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(f'''
            SELECT query, response, category, timestamp, usage_count
            FROM {self.table_name}
            WHERE query LIKE ?
            ORDER BY usage_count DESC, timestamp DESC
            LIMIT ?
        ''', (f'%{query}%', max_results))
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def query_all_agents(self, query, max_per_agent=3):
        """Query ALL agents' knowledge (cross-learning)"""
        conn = sqlite3.connect(str(SHARED_DB))
        conn.row_factory = sqlite3.Row
        
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%_knowledge'")
        tables = [row[0] for row in cursor.fetchall()]
        
        results = {}
        for table in tables:
            cursor = conn.execute(f'''
                SELECT query, response, source_agent, timestamp
                FROM {table}
                WHERE query LIKE ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (f'%{query}%', max_per_agent))
            rows = cursor.fetchall()
            if rows:
                agent_name = table.replace('_knowledge', '')
                results[agent_name] = [dict(row) for row in rows]
        
        conn.close()
        return results
    
    def get_stats(self):
        """Get memory statistics"""
        conn = sqlite3.connect(str(SHARED_DB))
        cursor = conn.execute(f"SELECT COUNT(*) FROM {self.table_name}")
        my_count = cursor.fetchone()[0]
        
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%_knowledge'")
        tables = [row[0] for row in cursor.fetchall()]
        
        all_counts = {}
        for table in tables:
            cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
            all_counts[table] = cursor.fetchone()[0]
        
        conn.close()
        return {"my_entries": my_count, "all_agents": all_counts}
