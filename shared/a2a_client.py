"""Shared A2A Client - WebSocket RPC Layer for Agent-to-Agent Communication

Connects to the A2A Server at 127.0.0.1:8766 for agent messaging.
Also provides WebClaw index search for offline/reference queries.
"""
import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional

PROJECT_ROOT = Path(__file__).parent.parent
INDEX_PATH = PROJECT_ROOT / "agents" / "webclaw" / "cache" / "url_index.json"
A2A_SERVER = "http://127.0.0.1:8766"


class A2AClient:
    """Real A2A RPC client for agent-to-agent messaging via the A2A server."""

    def __init__(self, server_url: str = A2A_SERVER):
        self.server_url = server_url.rstrip("/")

    def send_message(self, agent: str, task: str, timeout: int = 30) -> Dict:
        """Send a task to an agent via the A2A server. Returns the agent's response."""
        url = f"{self.server_url}/v1/message/{agent}"
        payload = json.dumps({"task": task}).encode("utf-8")

        try:
            req = urllib.request.Request(
                url,
                data=payload,
                headers={"Content-Type": "application/json", "User-Agent": "ClawPack-A2A-Client/1.0"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.URLError as e:
            return {"status": "error", "result": f"A2A server unreachable: {e.reason}"}
        except Exception as e:
            return {"status": "error", "result": str(e)}

    def health_check(self) -> Dict:
        """Check if A2A server is healthy."""
        try:
            req = urllib.request.Request(
                f"{self.server_url}/health",
                headers={"User-Agent": "ClawPack-A2A-Client/1.0"},
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    def list_agents(self) -> Dict:
        """List all registered agents."""
        try:
            req = urllib.request.Request(
                f"{self.server_url}/v1/agents",
                headers={"User-Agent": "ClawPack-A2A-Client/1.0"},
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            return {"status": "error", "result": str(e)}

    def search(self, query: str, max_results: int = 10) -> Dict:
        """Search the WebClaw chronicle index (offline fallback when A2A is down)."""
        return search_index(query, max_results)

    def categories(self) -> List:
        """List all categories in the WebClaw index."""
        return get_categories()

    def urls(self, category: str) -> List:
        """Get URLs for a WebClaw index category."""
        return get_urls_for_category(category)


# ---- WebClaw Index Functions (offline/reference) ----

def search_index(query: str, max_results: int = 10) -> dict:
    """Search the WebClaw category index (offline)."""

    if not INDEX_PATH.exists():
        return {"error": "Index not found", "results": []}

    try:
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            index = json.loads(f.read())
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON: {e}", "results": []}

    results = []
    query_lower = query.lower()

    for category, urls in index.items():
        if not isinstance(urls, list):
            continue
        if query_lower in category.lower():
            for url in urls:
                results.append({"category": category, "url": url, "relevance": "category_match"})
        for url in urls:
            if query_lower in url.lower():
                results.append({"category": category, "url": url, "relevance": "url_match"})
        if len(results) >= max_results:
            break

    return {"query": query, "total_categories": len(index), "results": results[:max_results]}


def get_categories() -> list:
    """List all categories in the index."""
    if not INDEX_PATH.exists():
        return []
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return list(json.loads(f.read()).keys())


def get_urls_for_category(category: str) -> list:
    """Get all URLs for a specific category."""
    if not INDEX_PATH.exists():
        return []
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.loads(f.read()).get(category, [])
