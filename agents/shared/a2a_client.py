"""Shared A2A Client - Query WebClaw Index"""
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
INDEX_PATH = PROJECT_ROOT / "agents" / "webclaw" / "cache" / "url_index.json"

def search_index(query: str, max_results: int = 10) -> dict:
    """Search the WebClaw category index"""
    
    if not INDEX_PATH.exists():
        return {"error": "Index not found", "results": []}
    
    try:
        with open(INDEX_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
            # Handle duplicate keys by parsing manually
            index = json.loads(content)
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON: {e}", "results": []}
    
    results = []
    query_lower = query.lower()
    
    # Search through all categories
    for category, urls in index.items():
        if isinstance(urls, list):
            # Check if query matches category
            if query_lower in category.lower():
                for url in urls:
                    results.append({
                        "category": category,
                        "url": url,
                        "relevance": "category_match"
                    })
            
            # Check individual URLs
            for url in urls:
                if query_lower in url.lower():
                    results.append({
                        "category": category,
                        "url": url,
                        "relevance": "url_match"
                    })
        
        if len(results) >= max_results:
            break
    
    return {
        "query": query,
        "total_categories": len(index),
        "results": results[:max_results]
    }

def get_categories() -> list:
    """List all categories in the index"""
    if not INDEX_PATH.exists():
        return []
    
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        index = json.loads(f.read())
    
    return list(index.keys())

def get_urls_for_category(category: str) -> list:
    """Get all URLs for a specific category"""
    if not INDEX_PATH.exists():
        return []
    
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        index = json.loads(f.read())
    
    return index.get(category, [])