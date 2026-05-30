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
        from agents.webclaw.core.chronicle_ledger import get_chronicle
        get_chronicle().record_fetch(url=f"agent:{agent_name}", context=context, source="_agent_helpers", metadata={"detail": str(error)[:500]})
    except Exception:
        try:
            print(f"[{agent_name}] {context}: {error}", flush=True)
        except Exception:
            pass

# ── Shared Learning ───────────────────────────────────────────────────────────

def learn(agent_name: str, query: str, result: str,
          source_type: str = "web_verified", confidence: float = 0.85,
          urls: list = None) -> bool:
    """
    Write a result to unified cross-agent memory. All 21 agents share this.
    MemoryGuard enforces: source must be web_verified or chronicle, confidence >= 0.75.
    Returns True if persisted, False if blocked by guard.

    Usage:
        from shared._agent_helpers import learn
        learn("lawclaw", "qualified immunity", result, "web_verified", 0.85, urls)
    """
    try:
        from shared.memory_guard import sanitize_memory_write
        check = sanitize_memory_write(agent_name, result[:100], source_type, confidence)
        if not check.get("allowed"):
            return False

        from shared.memory.unified_memory import UnifiedMemory
        from datetime import datetime, timezone

        mem = UnifiedMemory()
        fact = {
            "agent": agent_name,
            "query": query,
            "fact": result[:500],
            "source_type": source_type,
            "confidence": confidence,
            "urls": urls or [],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        mem._facts.append(fact)
        for word in query.lower().split():
            if len(word) > 3:
                if word not in mem._index:
                    mem._index[word] = []
                mem._index[word].append(len(mem._facts) - 1)
        mem._save_index()
        return True
    except Exception as e:
        _log(agent_name, "learn_error", str(e)[:200])
    return False


def recall_memory(agent_name: str, query: str, limit: int = 5) -> list:
    """
    Search unified memory for prior results across all agents.
    Returns list of fact dicts sorted by relevance and confidence.

    Usage:
        from shared._agent_helpers import recall_memory
        prior = recall_memory("lawclaw", "Miranda rights")
        for p in prior:
            print(p.get("agent"), p.get("fact")[:80])
    """
    try:
        from shared.memory.unified_memory import UnifiedMemory
        mem = UnifiedMemory()
        terms = query.lower().split()
        matches = []
        for fact in mem._facts:
            fact_text = (fact.get("fact", "") + " " + fact.get("query", "")).lower()
            score = sum(1 for t in terms if t in fact_text)
            if score > 0:
                matches.append((score, fact))
        matches.sort(key=lambda x: (-x[0], -x[1].get("confidence", 0)))
        return [m[1] for m in matches[:limit]]
    except Exception as e:
        _log(agent_name, "recall_error", str(e)[:200])
    return []


def smart_llm(agent_name: str, prompt: str, timeout: int = 120) -> str:
    """
    Full truth resolver pipeline: retriever + Chronicle + memory guard + conflict detection.
    Use this instead of llm() when you want verified answers with source trust scoring.

    Usage:
        from shared._agent_helpers import smart_llm
        result = smart_llm("lawclaw", "What is qualified immunity?")
    """
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        return agent.smart_ask(prompt)
    except Exception as e:
        _log(agent_name, "smart_llm_fallback", str(e)[:100])
        return llm(agent_name, prompt, timeout=timeout)
# ── Internal ──────────────────────────────────────────────────────────────────

def _log(agent_name: str, context: str, detail: str = "") -> None:
    """Internal logging — always silent on failure."""
    try:
        from agents.webclaw.core.chronicle_ledger import get_chronicle
        get_chronicle().record_fetch(url=f"agent:{agent_name}", context=context, source="_agent_helpers", metadata={"detail": str(detail)[:500]})
    except Exception:
        pass
