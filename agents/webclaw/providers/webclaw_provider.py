"""Webclaw Provider - Uses the 280 MB SQLite Chronicle Index"""
import sqlite3
from pathlib import Path
from typing import List, Optional, Dict


class WebclawProvider:
    """Fast search using pre-built SQLite index (1.5M terms, 20K files)"""
    
    def __init__(self):
        self.cache_dir = Path(__file__).parent.parent / "cache"
        self.db_path = self.cache_dir / "web_cache.db"
        self.references_path = Path(__file__).resolve().parent.parent / "references"
    
    def search(self, query: str, max_results: int = 20) -> str:
        """Search the SQLite index for matching terms"""
        if not query:
            return "No query provided"
        
        if not self.db_path.exists():
            return f"Index not found at {self.db_path}"
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        terms = query.lower().split()
        results = []
        seen_urls = set()
        
        for term in terms:
            cursor.execute("""
                SELECT DISTINCT si.url, si.frequency
                FROM search_index si
                WHERE si.term LIKE ?
                ORDER BY si.frequency DESC
                LIMIT ?
            """, (f"%{term}%", max_results))
            
            for row in cursor.fetchall():
                url = row[0]
                if url not in seen_urls:
                    seen_urls.add(url)
                    results.append({
                        "path": url,
                        "frequency": row[1]
                    })
        
        conn.close()
        
        if not results:
            return f"No results found for {query!r}"
        
        output = [f"Found {len(results)} results for {query!r}:\n"]
        for i, r in enumerate(results[:max_results], 1):
            output.append(f"  {i}. Path: {r["path"]}")
        
        return "\n".join(output)
    
    def search_with_context(self, query: str, max_results: int = 10, namespace: str = None) -> str:
        """Search with content snippets, namespace-scoped"""
        if not self.db_path.exists():
            return "Index not found"
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        terms = query.lower().split()
        results = []
        seen_urls = set()
        
        for term in terms:
            cursor.execute("""
                SELECT DISTINCT si.url, wc.content, si.frequency
                FROM search_index si
                LEFT JOIN web_cache wc ON si.url = wc.url
                WHERE si.term LIKE ? AND (? IS NULL OR si.url LIKE ?)
                ORDER BY si.frequency DESC
                LIMIT ?
            """, (f"%{term}%", namespace, f"%{namespace}%" if namespace else None, max_results))
            
            for row in cursor.fetchall():
                url = row[0]
                if url not in seen_urls:
                    seen_urls.add(url)
                    content = row[1] or ""
                    results.append({
                        "path": url,
                        "snippet": content,
                        "frequency": row[2]
                    })
        
        conn.close()
        
        if not results:
            return f"No results for {query!r}"
        
        output = [f"Found {len(results)} results:\n"]
        for i, r in enumerate(results[:max_results], 1):
            output.append(f"{i}. {r["path"]}")
            if r["snippet"]:
                output.append(f"   {r["snippet"]}...")
            output.append("")
        
        return "\n".join(output)
    
    def search_structured(self, query: str, max_results: int = 20, namespace: str = None) -> List[Dict]:
        """Return structured results for BM25 ranking. Compatible with core/retriever.py."""
        if not self.db_path.exists():
            return []
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        terms = query.lower().split()
        docs = []
        seen_urls = set()
        
        for term in terms:
            cursor.execute("""
                SELECT DISTINCT si.url, wc.content, si.frequency
                FROM search_index si
                LEFT JOIN web_cache wc ON si.url = wc.url
                WHERE si.term LIKE ? AND (? IS NULL OR si.url LIKE ?)
                ORDER BY si.frequency DESC
                LIMIT ?
            """, (f"%{term}%", namespace, f"%{namespace}%" if namespace else None, max_results))
            
            for row in cursor.fetchall():
                url = row[0]
                if url not in seen_urls:
                    seen_urls.add(url)
                    docs.append({
                        "url": url,
                        "context": row[1] or "",
                        "source": "web_cache",
                    })
        
        conn.close()
        return docs[:max_results]
