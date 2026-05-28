"""
lawclaw shared helpers — single source of truth for all commands.

Replaces duplicated _log(), llm(), chronicle_search(), webclaw_fetch(),
get_cl_token() functions across every command file.

Usage in any command:
    from agents.lawclaw.commands._helpers import log, llm, chronicle, webclaw, cl_get, cl_token

All LLM calls route through A2A → llmclaw → Sovereign Gateway. Constitutional.
All exceptions are logged. No silent failures. Constitutional.
"""
import requests
from pathlib import Path

A2A = "http://127.0.0.1:8766"
COURTLISTENER_API = "https://www.courtlistener.com/api/rest/v4"

# ── Audit logging ─────────────────────────────────────────────────────────────

def log(event: str, detail: str = "", agent: str = "lawclaw") -> None:
    """Constitutional audit logging. Never raises."""
    try:
        from agents.webclaw.core.chronicle_ledger import log_event
        log_event(agent=agent, event=event, detail=str(detail)[:500])
    except Exception:
        pass  # logging must never break commands


# ── LLM via Sovereign Gateway ─────────────────────────────────────────────────

def llm(prompt: str, timeout: int = 120) -> str:
    """
    Call llmclaw via A2A → Sovereign Gateway. Returns text or ''.
    Logs all failures. Never raises.
    """
    try:
        resp = requests.post(
            f"{A2A}/v1/message/llmclaw",
            json={"task": f"/llm {prompt}", "agent": "lawclaw"},
            timeout=timeout,
        )
        if resp.status_code == 200:
            result = resp.json().get("result", "")
            if result and len(result) > 20:
                return result
            log("llm_empty_result", f"len={len(result)}")
        else:
            log("llm_non200", str(resp.status_code))
    except requests.exceptions.Timeout:
        log("llm_timeout", f"{timeout}s")
    except requests.exceptions.ConnectionError:
        log("llm_connection_error")
    except Exception as e:
        log("llm_error", str(e)[:200])
    return ""


def smart_llm(prompt: str, query: str = "", timeout: int = 120) -> str:
    """
    LLM call that leverages BaseAgent.smart_ask() — full truth resolver pipeline.
    Use this when you want Chronicle + retriever + memory guard automatically.
    Falls back to llm() if smart_ask unavailable.
    """
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent("lawclaw")
        return agent.smart_ask(prompt)
    except Exception as e:
        log("smart_llm_fallback", str(e)[:100])
        return llm(prompt, timeout=timeout)


# ── WebClaw fetch via A2A ─────────────────────────────────────────────────────

def webclaw(url: str, timeout: int = 20) -> str:
    """
    Fetch a URL through webclaw A2A. Constitutional — no direct requests.get().
    Returns content string or ''. Logs all failures.
    """
    try:
        resp = requests.post(
            f"{A2A}/v1/message/webclaw",
            json={"task": f"fetch {url}", "agent": "lawclaw"},
            timeout=timeout,
        )
        if resp.status_code == 200:
            result = resp.json().get("result", "")
            if result:
                return result
            log("webclaw_empty_result", url)
        else:
            log("webclaw_non200", f"{resp.status_code} {url}")
    except requests.exceptions.Timeout:
        log("webclaw_timeout", url)
    except requests.exceptions.ConnectionError:
        log("webclaw_connection_error", url)
    except Exception as e:
        log("webclaw_error", f"{e} {url}")
    return ""


# ── Chronicle search ──────────────────────────────────────────────────────────

def chronicle(query: str, limit: int = 10) -> list:
    """
    Search Chronicle index. Returns list of result dicts or [].
    Logs all failures.
    """
    try:
        from agents.webclaw.core.chronicle_ledger import get_chronicle
        c = get_chronicle()
        results = c.recover_by_context(query, limit=limit)
        return results if results else []
    except ImportError:
        log("chronicle_import_error")
    except Exception as e:
        log("chronicle_error", str(e)[:200])
    return []


def chronicle_context(query: str, limit: int = 10, max_chars: int = 800) -> str:
    """
    Search Chronicle and return formatted context string for LLM prompts.
    Returns '' if nothing found.
    """
    results = chronicle(query, limit=limit)
    if not results:
        return ""
    parts = []
    for r in results[:limit]:
        ctx = r["context"] if isinstance(r, dict) else str(r)
        url = r.get("url", "") if isinstance(r, dict) else ""
        entry = f"SOURCE: {url}\n{ctx[:max_chars]}" if url else ctx[:max_chars]
        parts.append(entry)
    return "\n---\n".join(parts)


def chronicle_urls(query: str, limit: int = 10) -> list:
    """Return list of URLs from Chronicle results for a query."""
    results = chronicle(query, limit=limit)
    urls = []
    for r in results:
        if isinstance(r, dict):
            url = r.get("url", "")
            if url and url.startswith("http"):
                urls.append(url)
    return list(dict.fromkeys(urls))  # deduplicated, order preserved


# ── CourtListener API ─────────────────────────────────────────────────────────

def cl_token() -> str:
    """Read CourtListener API token from .env. Returns '' if not found."""
    try:
        env_path = Path(__file__).parent.parent.parent.parent / ".env"
        for line in env_path.read_text().split("\n"):
            if "COURTLISTENER_TOKEN" in line and "=" in line:
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except Exception as e:
        log("cl_token_error", str(e)[:100])
    return ""


def cl_get(path: str, params: dict = None, timeout: int = 15) -> list:
    """
    Generic CourtListener API GET. Returns list of results or [].
    Logs all failures including non-200 status codes.
    """
    token = cl_token()
    if not token:
        log("cl_no_token", path)
        return []
    try:
        r = requests.get(
            f"{COURTLISTENER_API}/{path}",
            params=params or {},
            headers={"Authorization": f"Token {token}", "User-Agent": "LawClaw/1.0"},
            timeout=timeout,
        )
        if r.status_code == 200:
            data = r.json()
            return data.get("results", [])
        log("cl_non200", f"{r.status_code} {path}")
    except requests.exceptions.Timeout:
        log("cl_timeout", path)
    except requests.exceptions.ConnectionError:
        log("cl_connection_error", path)
    except Exception as e:
        log("cl_error", f"{e} {path}")
    return []


def cl_get_one(path: str, record_id, timeout: int = 15) -> dict:
    """
    Fetch a single CourtListener record by ID. Returns dict or {}.
    """
    token = cl_token()
    if not token:
        return {}
    try:
        r = requests.get(
            f"{COURTLISTENER_API}/{path}/{record_id}/",
            headers={"Authorization": f"Token {token}", "User-Agent": "LawClaw/1.0"},
            timeout=timeout,
        )
        if r.status_code == 200:
            return r.json()
        log("cl_get_one_non200", f"{r.status_code} {path}/{record_id}")
    except Exception as e:
        log("cl_get_one_error", str(e)[:200])
    return {}


def cl_search(query: str, search_type: str = "o", courts: str = None,
              order_by: str = "-score", limit: int = 10) -> list:
    """
    Search CourtListener full-text search endpoint.
    search_type: 'o' opinions, 'd' dockets, 'r' recap docs, 'p' people
    courts: comma-separated court codes e.g. 'scotus,ca9'
    Returns list of result dicts or [].
    """
    token = cl_token()
    if not token:
        return []
    params = {
        "q": query,
        "type": search_type,
        "order_by": order_by,
        "page_size": limit,
    }
    if courts:
        params["court"] = courts
    try:
        r = requests.get(
            f"{COURTLISTENER_API}/search/",
            params=params,
            headers={"Authorization": f"Token {token}", "User-Agent": "LawClaw/1.0"},
            timeout=30,
        )
        if r.status_code == 200:
            return r.json().get("results", [])
        log("cl_search_non200", f"{r.status_code} q={query}")
    except requests.exceptions.Timeout:
        log("cl_search_timeout", query)
    except Exception as e:
        log("cl_search_error", str(e)[:200])
    return []


# ── Cross-agent delegation ────────────────────────────────────────────────────

def delegate(agent_name: str, task: str, timeout: int = 60) -> str:
    """
    Delegate a task to another agent via A2A. Constitutional cross-agent call.
    Returns result string or ''. Logs failures.

    Usage:
        doc = delegate("docuclaw", f"/create legal brief: {summary}")
        chart = delegate("plotclaw", f"/plot case timeline: {data}")
    """
    try:
        resp = requests.post(
            f"{A2A}/v1/message/{agent_name}",
            json={"task": task, "agent": "lawclaw"},
            timeout=timeout,
        )
        if resp.status_code == 200:
            return resp.json().get("result", "")
        log("delegate_non200", f"{resp.status_code} → {agent_name}")
    except requests.exceptions.Timeout:
        log("delegate_timeout", f"{agent_name} {timeout}s")
    except requests.exceptions.ConnectionError:
        log("delegate_connection_error", agent_name)
    except Exception as e:
        log("delegate_error", f"{agent_name}: {e}")
    return ""


# ── Jurisdiction filesystem ───────────────────────────────────────────────────

def jurisdiction_root() -> Path:
    """Return path to jurisdictions/us directory."""
    return (
        Path(__file__).parent.parent.parent.parent
        / "agents" / "webclaw" / "references" / "lawclaw" / "jurisdictions" / "us"
    )