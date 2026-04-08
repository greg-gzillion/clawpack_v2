"""Caching system for WebClaw - store fetched content to avoid repeated requests"""

import hashlib
import json
import sqlite3
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class WebCache:
    """SQLite-based cache for web content with TTL"""
    
    def __init__(self, cache_dir: Path = None):
        if cache_dir is None:
            cache_dir = Path(__file__).parent.parent / "cache"
        cache_dir.mkdir(exist_ok=True)
        
        self.db_path = cache_dir / "web_cache.db"
        self._init_db()
        self._clean_old_entries()
    
    def _init_db(self):
        """Initialize cache database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    url TEXT PRIMARY KEY,
                    content TEXT,
                    content_type TEXT,
                    size INTEGER,
                    fetched_at REAL,
                    expires_at REAL,
                    hit_count INTEGER DEFAULT 1
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_expires ON cache(expires_at)")
    
    def _get_url_hash(self, url: str) -> str:
        """Get hash of URL for key"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def get(self, url: str, max_age_hours: int = 24) -> Optional[Dict[str, Any]]:
        """Get cached content if not expired"""
        url_hash = self._get_url_hash(url)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT content, content_type, size, fetched_at, expires_at, hit_count FROM cache WHERE url = ?",
                (url,)
            )
            row = cursor.fetchone()
            
            if row:
                content, content_type, size, fetched_at, expires_at, hit_count = row
                
                # Check if expired
                if time.time() > expires_at:
                    # Delete expired entry
                    conn.execute("DELETE FROM cache WHERE url = ?", (url,))
                    return None
                
                # Update hit count
                conn.execute("UPDATE cache SET hit_count = hit_count + 1 WHERE url = ?", (url,))
                conn.commit()
                
                return {
                    "content": content,
                    "content_type": content_type,
                    "size": size,
                    "fetched_at": fetched_at,
                    "expires_at": expires_at,
                    "hit_count": hit_count
                }
        
        return None
    
    def set(self, url: str, content: str, content_type: str = "text/html", ttl_hours: int = 24):
        """Cache content with TTL"""
        url_hash = self._get_url_hash(url)
        fetched_at = time.time()
        expires_at = fetched_at + (ttl_hours * 3600)
        size = len(content)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO cache (url, content, content_type, size, fetched_at, expires_at, hit_count)
                VALUES (?, ?, ?, ?, ?, ?, 1)
            """, (url, content, content_type, size, fetched_at, expires_at))
            conn.commit()
    
    def _clean_old_entries(self):
        """Remove expired entries"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM cache WHERE expires_at < ?", (time.time(),))
            conn.commit()
    
    def clear(self):
        """Clear entire cache"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM cache")
            conn.commit()
    
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*), SUM(hit_count) FROM cache")
            count, total_hits = cursor.fetchone()
            return {
                "entries": count or 0,
                "total_hits": total_hits or 0,
                "avg_hits": (total_hits / count) if count else 0
            }

# Singleton
_cache = None

def get_cache():
    global _cache
    if _cache is None:
        _cache = WebCache()
    return _cache
