"""
shared/_agent_helpers.py — Empire-wide agent utilities.

One import connects any agent to the full Clawpack infrastructure:
    from shared._agent_helpers import llm, smart, chronicle, web, delegate, log_err

Replaces per-agent reimplementations of LLM calls, web search,
Chronicle lookup, and cross-agent delegation.

Constitutional: all LLM calls route through Sovereign Gateway.
All exceptions logged. No silent failures.
"""
from typing import Optional


# ── LLM via Sovereign Gateway ─────────────────────────────────────────────────

def llm(agent_name: str, prompt: str, timeout: int = 120) -> str:
    """
    Call LLM through Sovereign Gateway. Chronicle-enriched, budget-tracked.
    Equivalent to BaseAgent.ask_llm() without needing a BaseAgent instance.

    Usage:
        from shared._agent_helpers import llm
        result = llm("myclaw", "Explain this concept: ...")
    """
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        return agent.ask_llm(prompt)
    except Exception as e:
        _log(agent_name, "llm_error", str(e)[:200])
    return ""


def smart(agent_name: str, prompt: str) -> str:
    """
    Full truth resolver pipeline: retriever + Chronicle + memory guard + conflict detection.
    Equivalent to BaseAgent.smart_ask().

    Usage:
        from shared._agent_helpers import smart
        result = smart("myclaw", "What is qualified immunity?")
    """
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        return agent.smart_ask(prompt)
    except Exception as e:
        _log(agent_name, "smart_error", str(e)[:200])
    return ""


# ── Chronicle search ──────────────────────────────────────────────────────────

def chronicle(agent_name: str, query: str, limit: int = 10) -> list:
    """
    Search 448MB Chronicle SQLite index.
    Returns list of result dicts with 'context' and 'url' keys.

    Usage:
        from shared._agent_helpers import chronicle
        results = chronicle("myclaw", "Miranda v Arizona", limit=5)
        for r in results:
            print(r.get("context", "")[:200])
    """
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        return agent.search_chronicle(query, limit) or []
    except Exception as e:
        _log(agent_name, "chronicle_error", str(e)[:200])
    return []


def chronicle_text(agent_name: str, query: str, limit: int = 10,
                   max_chars: int = 800) -> str:
    """
    Search Chronicle and return formatted string for LLM prompts.

    Usage:
        ctx = chronicle_text("myclaw", "Fourth Amendment search seizure")
        result = llm("myclaw", f"Analyze this: ...\n\nContext:\n{ctx}")
    """
    results = chronicle(agent_name, query, limit)
    if not results:
        return ""
    parts = []
    for r in results[:limit]:
        ctx = r.get("context", "") if isinstance(r, dict) else str(r)
        url = r.get("url", "") if isinstance(r, dict) else ""
        entry = f"SOURCE: {url}\n{ctx[:max_chars]}" if url else ctx[:max_chars]
        parts.append(entry)
    return "\n---\n".join(parts)


# ── Web search ────────────────────────────────────────────────────────────────

def web(agent_name: str, query: str, max_results: int = 10) -> str:
    """
    Search the web via webclaw. Results indexed to Chronicle automatically.

    Usage:
        from shared._agent_helpers import web
        results = web("myclaw", "qualified immunity Supreme Court 2024")
    """
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        return agent.search_web(query, max_results)
    except Exception as e:
        _log(agent_name, "web_error", str(e)[:200])
    return ""


def fetch(agent_name: str, url: str, timeout: int = 20) -> str:
    """
    Fetch a URL through webclaw A2A. Constitutional — no direct requests.get().

    Usage:
        from shared._agent_helpers import fetch
        content = fetch("myclaw", "https://www.fjc.gov/history/judges/sotomayor")
    """
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        return agent.call_agent("webclaw", f"fetch {url}", timeout=timeout)
    except Exception as e:
        _log(agent_name, "fetch_error", str(e)[:200])
    return ""


# ── Cross-agent delegation ────────────────────────────────────────────────────

def delegate(from_agent: str, to_agent: str, task: str,
             timeout: int = 60) -> str:
    """
    Delegate a task to another agent via A2A. Constitutional cross-agent call.
    Returns result string or '' on failure.

    Usage:
        from shared._agent_helpers import delegate

        # lawclaw → docuclaw
        doc = delegate("lawclaw", "docuclaw", "/create legal brief: ...")

        # mediclaw → lawclaw
        legal = delegate("mediclaw", "lawclaw", "/law HIPAA patient rights")

        # any agent → webclaw
        page = delegate("myclaw", "webclaw", "fetch https://...")
    """
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(from_agent)
        return agent.call_agent(to_agent, task, timeout=timeout)
    except Exception as e:
        _log(from_agent, f"delegate_to_{to_agent}_error", str(e)[:200])
    return ""


# ── Memory ────────────────────────────────────────────────────────────────────

def remember(agent_name: str, key: str, value: str) -> None:
    """
    Store a value in agent state (persists to data/shared_memory.json).

    Usage:
        remember("myclaw", "last_query", "Miranda v Arizona")
    """
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        agent.learn(key, value)
    except Exception as e:
        _log(agent_name, "remember_error", str(e)[:200])


def recall(agent_name: str, key: str) -> Optional[str]:
    """
    Retrieve a stored value from agent state.

    Usage:
        last = recall("myclaw", "last_query")
    """
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        return agent.recall(key)
    except Exception as e:
        _log(agent_name, "recall_error", str(e)[:200])
    return None


def learn_fact(agent_name: str, fact: str) -> None:
    """
    Write a fact to unified cross-agent memory (all 21 agents share this).
    Facts are searchable by any agent via recall_facts().

    Usage:
        learn_fact("lawclaw", "Qualified immunity requires clearly established rights")
    """
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        agent.learn_fact(fact)
    except Exception as e:
        _log(agent_name, "learn_fact_error", str(e)[:200])


# ── Chronicle recording ───────────────────────────────────────────────────────

def record(agent_name: str, url: str, context: str) -> None:
    """
    Index a URL and its content to Chronicle.
    Makes this content searchable by all agents.

    Usage:
        record("lawclaw", "https://fjc.gov/judges/sotomayor",
               "Sonia Sotomayor appointed 2009 by Obama, SCOTUS")
    """
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        agent.record_in_chronicle(url=url, context=context, source=agent_name)
    except Exception as e:
        _log(agent_name, "record_error", str(e)[:200])


# ── Error logging ─────────────────────────────────────────────────────────────

def log_err(agent_name: str, context: str, error: str) -> None:
    """
    Constitutional audit logging. Never raises.

    Usage:
        except Exception as e:
            log_err("myclaw", "fetch_timeout", str(e)[:200])
    """
    try:
        from agents.webclaw.core.chronicle_ledger import log_event
        log_event(agent=agent_name, event=context, detail=str(error)[:500])
    except Exception:
        try:
            print(f"[{agent_name}] {context}: {error}", flush=True)
        except Exception:
            pass


# ── Internal ──────────────────────────────────────────────────────────────────

def _log(agent_name: str, context: str, detail: str = "") -> None:
    """Internal logging — always silent on failure."""
    try:
        from agents.webclaw.core.chronicle_ledger import log_event
        log_event(agent=agent_name, event=context, detail=str(detail)[:500])
    except Exception:
        pass
