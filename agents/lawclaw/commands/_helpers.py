"""lawclaw shared helpers — constitutional cross-command utilities.

All LLM calls route through agent context → Sovereign Gateway. Constitutional.
All cross-agent calls use agent.call_agent() with circuit breaker protection.
All exceptions are logged. No silent failures. Constitutional.

Usage in commands:
    from agents.lawclaw.commands._helpers import llm, webclaw, chronicle, delegate
    result = llm(prompt, agent=agent)
    result = webclaw(url, agent=agent)
"""
from pathlib import Path
import requests  # Only for CourtListener API (external, not A2A)

COURTLISTENER_API = "https://www.courtlistener.com/api/rest/v4"


def log(event: str, detail: str = "", agent_name: str = "lawclaw") -> None:
    """Constitutional audit logging. Never raises."""
    try:
        from agents.webclaw.core.chronicle_ledger import get_chronicle
        c = get_chronicle()
        c.record_fetch(url=f"lawclaw://{event}", context=str(detail)[:500], source=agent_name)
    except Exception:
        pass


def llm(prompt: str, timeout: int = 120, agent=None) -> str:
    """Call Sovereign Gateway via agent context. Returns text or ''."""
    if agent and hasattr(agent, 'ask_llm'):
        try:
            return agent.ask_llm(prompt)
        except Exception as e:
            log("llm_error", str(e)[:200])
            return ""
    return ""


def webclaw(url: str, timeout: int = 20, agent=None) -> str:
    """Fetch a URL through webclaw via agent context. Constitutional."""
    if agent and hasattr(agent, 'call_agent'):
        try:
            result = agent.call_agent("webclaw", f"fetch {url}", timeout=timeout)
            return str(result) if result else ""
        except Exception as e:
            log("webclaw_error", f"{url}: {str(e)[:100]}")
            return ""
    return ""


def chronicle(query: str, limit: int = 10, agent=None) -> list:
    """Search Chronicle via agent context."""
    if agent and hasattr(agent, 'search_chronicle'):
        try:
            return agent.search_chronicle(query, limit=limit)
        except Exception as e:
            log("chronicle_error", str(e)[:200])
            return []
    return []


def chronicle_context(query: str, limit: int = 10, max_chars: int = 800, agent=None) -> str:
    """Return concatenated context from Chronicle results."""
    results = chronicle(query, limit=limit, agent=agent)
    if not results:
        return ""
    lines = []
    for r in results:
        ctx = r.get("context", "") if isinstance(r, dict) else str(r)
        if ctx:
            lines.append(ctx[:max_chars])
    return "\n".join(lines)


def chronicle_urls(query: str, limit: int = 10, agent=None) -> list:
    """Return list of URLs from Chronicle results."""
    results = chronicle(query, limit=limit, agent=agent)
    urls = []
    for r in results:
        url = r.get("url", "") if isinstance(r, dict) else ""
        if url and "https://" in url:
            urls.append(url)
    return urls


def delegate(agent_name: str, task: str, timeout: int = 60, agent=None) -> str:
    """Delegate to another agent via agent context. Circuit breaker protected."""
    if agent and hasattr(agent, 'call_agent'):
        try:
            result = agent.call_agent(agent_name, task, timeout=timeout)
            return str(result) if result else ""
        except Exception as e:
            log("delegate_error", f"{agent_name}: {str(e)[:100]}")
            return ""
    return ""


def cl_token() -> str:
    """Read CourtListener API token from .env."""
    try:
        env_path = Path(__file__).parent.parent.parent.parent / ".env"
        if env_path.exists():
            for line in env_path.read_text().split("\n"):
                if "COURTLISTENER" in line.upper() and "=" in line:
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    except Exception:
        pass
    return ""


def cl_get(path: str, params: dict = None, timeout: int = 15) -> list:
    """CourtListener API GET — external API, not A2A."""
    token = cl_token()
    headers = {"Authorization": f"Token {token}"} if token else {}
    try:
        r = requests.get(f"{COURTLISTENER_API}/{path}", headers=headers, params=params, timeout=timeout)
        if r.status_code == 200:
            data = r.json()
            return data.get("results", []) if isinstance(data, dict) else []
        log("cl_non200", f"{r.status_code} {path}")
    except requests.exceptions.Timeout:
        log("cl_timeout", path)
    except requests.exceptions.ConnectionError:
        log("cl_connection_error", path)
    return []


def cl_get_one(path: str, record_id, timeout: int = 15) -> dict:
    """CourtListener single record."""
    token = cl_token()
    headers = {"Authorization": f"Token {token}"} if token else {}
    try:
        r = requests.get(f"{COURTLISTENER_API}/{path}/{record_id}/", headers=headers, timeout=timeout)
        if r.status_code == 200:
            return r.json()
        log("cl_non200", f"{r.status_code} {path}/{record_id}")
    except requests.exceptions.Timeout:
        log("cl_timeout", f"{path}/{record_id}")
    except requests.exceptions.ConnectionError:
        log("cl_connection_error", f"{path}/{record_id}")
    return {}


def cl_search(query: str, search_type: str = "o", courts: str = None,
              order_by: str = "-score", limit: int = 10) -> list:
    """CourtListener search."""
    params = {"q": query, "type": search_type, "order_by": order_by}
    if courts:
        params["court"] = courts
    return cl_get("search", params=params)[:limit]


def memory_write(command: str, query: str, result_summary: str,
                 source_type: str = "web_verified", confidence: float = 0.85) -> bool:
    """Write to unified memory via _memory bridge."""
    try:
        from agents.lawclaw.commands._memory import remember
        return remember(command=command, query=query, result_summary=result_summary,
                        source_type=source_type, confidence=confidence)
    except Exception:
        return False


def jurisdiction_root() -> Path:
    """Return path to jurisdictions/us directory."""
    return Path(__file__).parent.parent.parent.parent / "agents" / "webclaw" / "references" / "lawclaw" / "jurisdictions" / "us"
