"""DataClaw Search Cache — canonical cache for all agent web searches.

Architecture:
  dataclaw/cache/{agent_name}/{query_hash}.json
  
Every web search by any agent is cached here. Subsequent identical
searches return cached results without hitting the web or using tokens.
"""
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

CACHE_ROOT = Path(__file__).parent.parent / "agents" / "dataclaw" / "cache"
CACHE_ROOT.mkdir(parents=True, exist_ok=True)


def _query_hash(query: str) -> str:
    """Create a short hash for the query to use as filename."""
    return hashlib.sha256(query.lower().strip().encode()).hexdigest()[:16]


def cache_search(agent_name: str, query: str, results: str, urls: list = None) -> str:
    """Cache a web search result for an agent.
    
    Args:
        agent_name: e.g. 'lawclaw', 'mediclaw'
        query: The search query
        results: The raw search results text
        urls: List of URLs found
    
    Returns:
        Path to the cache file
    """
    agent_dir = CACHE_ROOT / agent_name
    agent_dir.mkdir(parents=True, exist_ok=True)
    
    qhash = _query_hash(query)
    cache_file = agent_dir / f"{qhash}.json"
    
    entry = {
        "agent": agent_name,
        "query": query,
        "query_hash": qhash,
        "results": results,  # Truncate to reasonable size
        "urls": urls or [],
        "cached_at": datetime.now(timezone.utc).isoformat(),
        "hit_count": 1,
    }
    
    # If file exists, increment hit count instead of overwriting
    if cache_file.exists():
        try:
            existing = json.loads(cache_file.read_text())
            entry["hit_count"] = existing.get("hit_count", 0) + 1
            entry["cached_at"] = existing.get("cached_at", entry["cached_at"])
        except Exception:
            pass
    
    cache_file.write_text(json.dumps(entry, indent=2, default=str))
    return str(cache_file.relative_to(CACHE_ROOT.parent))


def get_cached(agent_name: str, query: str) -> Optional[dict]:
    """Retrieve a cached search result. Returns None if not found or expired."""
    agent_dir = CACHE_ROOT / agent_name
    if not agent_dir.exists():
        return None
    
    qhash = _query_hash(query)
    cache_file = agent_dir / f"{qhash}.json"
    
    if not cache_file.exists():
        return None
    
    try:
        entry = json.loads(cache_file.read_text())
        
        # Check staleness — cache valid for 24 hours
        cached_time = datetime.fromisoformat(entry["cached_at"])
        age = datetime.now(timezone.utc) - cached_time
        if age.days > 1:
            return None  # Expired
        
        # Increment hit count
        entry["hit_count"] = entry.get("hit_count", 0) + 1
        cache_file.write_text(json.dumps(entry, indent=2, default=str))
        
        return entry
    except Exception:
        return None


def get_cache_stats(agent_name: str = None) -> dict:
    """Get cache statistics."""
    stats = {"agents": {}, "total_entries": 0, "total_hits": 0}
    
    for agent_dir in CACHE_ROOT.iterdir():
        if not agent_dir.is_dir(): continue
        name = agent_dir.name
        entries = list(agent_dir.glob("*.json"))
        hits = 0
        for f in entries:
            try:
                hits += json.loads(f.read_text()).get("hit_count", 0)
            except Exception:
                pass
        stats["agents"][name] = {"entries": len(entries), "hits": hits}
        stats["total_entries"] += len(entries)
        stats["total_hits"] += hits
    
    if agent_name:
        return stats["agents"].get(agent_name, {"entries": 0, "hits": 0})
    return stats
