"""
shared/_agent_helpers.py — Empire-wide agent utilities.

One import connects any agent to the full Clawpack infrastructure:
    from shared._agent_helpers import llm, cached, chronicle, delegate, log_err

PREFERRED METHODS (use these):
    cached()    — cache-first retrieval with WebClaw BM25 fallback
    llm()       — Sovereign Gateway LLM call
    chronicle() — 448MB FTS5 knowledge base search
    delegate()  — cross-agent delegation with circuit breaker
    log_err()   — constitutional audit logging

LEGACY METHODS (still work, prefer cached() instead):
    web()       — direct WebClaw search (bypasses cache)
    fetch()     — URL fetch via WebClaw

ADVANCED METHODS (use with caution — depend on dormant modules):
    smart()     — full truth resolver pipeline

Constitutional: all LLM calls route through Sovereign Gateway.
All exceptions logged. No silent failures.
"""
from typing import Optional


# ── Cache-First Retrieval (PREFERRED) ─────────────────────────────────

def cached(agent_name: str, query: str) -> str:
    """Cache-first retrieval with WebClaw BM25 fallback.
    
    Flow: DataClaw cache check -> WebClaw BM25 -> cache write.
    Returns [CACHED] marker on cache hits.
    Preserves BM25 score:, source:, deduped from markers.
    This is the primary retrieval method for all agents.
    """
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        return agent.cached_search(query)
    except Exception as e:
        _log(agent_name, "cached_error", str(e)[:200])
    return ""


# ── LLM via Sovereign Gateway ────────────────────────────────────────────

def llm(agent_name: str, prompt: str, timeout: int = 120) -> str:
    """Call LLM through Sovereign Gateway. Budget-tracked, constitutional."""
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        return agent.ask_llm(prompt)
    except Exception as e:
        _log(agent_name, "llm_error", str(e)[:200])
    return ""


# ── Chronicle search ─────────────────────────────────────────────────────

def chronicle(agent_name: str, query: str, limit: int = 10) -> list:
    """Search 448MB Chronicle SQLite FTS5 index. Returns list of result dicts."""
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        return agent.search_chronicle(query, limit) or []
    except Exception as e:
        _log(agent_name, "chronicle_error", str(e)[:200])
    return []


# ── Cache operations ─────────────────────────────────────────────────────

def cache_get(agent_name: str, query: str):
    """Retrieve a cached result from DataClaw. Returns None if not found."""
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        return agent.get_cached_result(agent_name, query)
    except Exception as e:
        _log(agent_name, "cache_get_error", str(e)[:200])
    return None


def cache_put(agent_name: str, query: str, results: str) -> bool:
    """Cache a result to DataClaw. Returns True on success."""
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        agent.cache_result(agent_name, query, results)
        return True
    except Exception as e:
        _log(agent_name, "cache_put_error", str(e)[:200])
    return False


# ── Web search (LEGACY — prefer cached()) ────────────────────────────────

def web(agent_name: str, query: str, max_results: int = 10) -> str:
    """Search the web via webclaw. Prefer cached() for cache-first retrieval."""
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        return agent.search_web(query, max_results)
    except Exception as e:
        _log(agent_name, "web_error", str(e)[:200])
    return ""


def fetch(agent_name: str, url: str, timeout: int = 20) -> str:
    """Fetch a URL through webclaw A2A. Constitutional — no direct requests."""
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        return agent.call_agent("webclaw", f"fetch {url}", timeout=timeout)
    except Exception as e:
        _log(agent_name, "fetch_error", str(e)[:200])
    return ""


# ── Cross-agent delegation ───────────────────────────────────────────────

def delegate(from_agent: str, to_agent: str, task: str,
             timeout: int = 60) -> str:
    """Delegate a task to another agent via A2A. Constitutional."""
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(from_agent)
        return agent.call_agent(to_agent, task, timeout=timeout)
    except Exception as e:
        _log(from_agent, f"delegate_to_{to_agent}_error", str(e)[:200])
    return ""


# ── Error logging ────────────────────────────────────────────────────────

def log_err(agent_name: str, context: str, error: str) -> None:
    """Constitutional audit logging. Never raises."""
    try:
        from agents.webclaw.core.chronicle_ledger import get_chronicle
        get_chronicle().record_fetch(
            url=f"agent:{agent_name}",
            context=context,
            source="_agent_helpers",
            metadata={"detail": str(error)[:500]},
        )
    except Exception:
        try:
            print(f"[{agent_name}] {context}: {error}", flush=True)
        except Exception:
            pass


# ── Advanced (use with caution) ──────────────────────────────────────────

def smart(agent_name: str, prompt: str) -> str:
    """Full truth resolver pipeline. Depends on dormant memory modules."""
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        return agent.smart_ask(prompt)
    except Exception as e:
        _log(agent_name, "smart_error", str(e)[:200])
    return ""


# ── Internal ─────────────────────────────────────────────────────────────

def _log(agent_name: str, context: str, detail: str = "") -> None:
    """Internal logging — always silent on failure."""
    try:
        from agents.webclaw.core.chronicle_ledger import get_chronicle
        get_chronicle().record_fetch(
            url=f"agent:{agent_name}",
            context=context,
            source="_agent_helpers",
            metadata={"detail": str(detail)[:500]},
        )
    except Exception:
        pass
