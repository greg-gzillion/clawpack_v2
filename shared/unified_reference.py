"""Unified Reference System - All agents can access"""

import sqlite3
from pathlib import Path
from datetime import datetime

class UnifiedReference:
    """Central reference system for all agents"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = Path.home() / ".claw_memory" / "unified_references.db"
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database with schema"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        schema_path = Path(__file__).parent / "reference_schema.sql"
        if schema_path.exists():
            with open(schema_path, 'r') as f:
                schema = f.read()
            self._execute(schema)
    
    def _get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def _execute(self, query, params=None):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor
    
    def add_reference(self, agent_name, category, title, content, tags=None):
        """Add a reference for an agent"""
        query = """
            INSERT INTO references_index (agent_name, category, title, content, tags)
            VALUES (?, ?, ?, ?, ?)
        """
        tags_str = ",".join(tags) if tags else ""
        self._execute(query, (agent_name, category, title, content, tags_str))
        return True
    
    def search(self, query_text, agent_filter=None):
        """Search across all references"""
        sql = """
            SELECT agent_name, category, title, content, tags
            FROM references_index
            WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?
        """
        params = [f"%{query_text}%", f"%{query_text}%", f"%{query_text}%"]
        
        if agent_filter:
            sql += " AND agent_name = ?"
            params.append(agent_filter)
        
        results = self._execute(sql, params).fetchall()
        return results
    
    def share_knowledge(self, from_agent, to_agent, topic, content):
        """Share knowledge between agents"""
        query = """
            INSERT INTO agent_knowledge_sharing (from_agent, to_agent, knowledge_topic, knowledge_content)
            VALUES (?, ?, ?, ?)
        """
        self._execute(query, (from_agent, to_agent, topic, content))
        return True
    
    def get_shared_knowledge(self, agent_name):
        """Get knowledge shared with an agent"""
        query = """
            SELECT from_agent, knowledge_topic, knowledge_content, shared_at
            FROM agent_knowledge_sharing
            WHERE to_agent = ? AND acknowledged = 0
            ORDER BY shared_at DESC
        """
        return self._execute(query, (agent_name,)).fetchall()
    
    def get_agent_references(self, agent_name):
        """Get all references for a specific agent"""
        query = """
            SELECT category, title, content, tags
            FROM references_index
            WHERE agent_name = ?
            ORDER BY category, title
        """
        return self._execute(query, (agent_name,)).fetchall()

# Singleton instance
_unified_ref = None

def get_reference_system():
    global _unified_ref
    if _unified_ref is None:
        _unified_ref = UnifiedReference()
    return _unified_ref
