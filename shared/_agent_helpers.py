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


# ── LLM via Sovereign Gateway ────────────────────────────────────────────

def llm(agent_name: str, prompt: str, timeout: int = 120) -> str:
    """Call LLM through Sovereign Gateway. Chronicle-enriched, budget-tracked."""
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        return agent.ask_llm(prompt)
    except Exception as e:
        _log(agent_name, "llm_error", str(e)[:200])
    return ""


def smart(agent_name: str, prompt: str) -> str:
    """Full truth resolver pipeline: retriever + Chronicle + memory guard + conflict detection."""
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        return agent.smart_ask(prompt)
    except Exception as e:
        _log(agent_name, "smart_error", str(e)[:200])
    return ""


# ── Chronicle search ─────────────────────────────────────────────────────

def chronicle(agent_name: str, query: str, limit: int = 10) -> list:
    """Search 448MB Chronicle SQLite index. Returns list of result dicts."""
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        return agent.search_chronicle(query, limit) or []
    except Exception as e:
        _log(agent_name, "chronicle_error", str(e)[:200])
    return []


def chronicle_text(agent_name: str, query: str, limit: int = 10,
                   max_chars: int = 800) -> str:
    """Search Chronicle and return formatted string for LLM prompts."""
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


# ── Web search ───────────────────────────────────────────────────────────

def web(agent_name: str, query: str, max_results: int = 10) -> str:
    """Search the web via webclaw. Results indexed to Chronicle automatically."""
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        return agent.search_web(query, max_results)
    except Exception as e:
        _log(agent_name, "web_error", str(e)[:200])
    return ""


def fetch(agent_name: str, url: str, timeout: int = 20) -> str:
    """Fetch a URL through webclaw A2A. Constitutional — no direct requests.get()."""
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
    """Delegate a task to another agent via A2A. Constitutional cross-agent call."""
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(from_agent)
        return agent.call_agent(to_agent, task, timeout=timeout)
    except Exception as e:
        _log(from_agent, f"delegate_to_{to_agent}_error", str(e)[:200])
    return ""


# ── Memory ───────────────────────────────────────────────────────────────

def remember(agent_name: str, key: str, value: str) -> None:
    """Store a value in agent state (persists to runtime/shared_memory.json)."""
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        agent.learn(key, value)
    except Exception as e:
        _log(agent_name, "remember_error", str(e)[:200])


def recall(agent_name: str, key: str) -> Optional[str]:
    """Retrieve a stored value from agent state."""
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        return agent.recall(key)
    except Exception as e:
        _log(agent_name, "recall_error", str(e)[:200])
    return None


def learn_fact(agent_name: str, fact: str) -> None:
    """Write a fact to unified cross-agent memory (all 21 agents share this)."""
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        agent.learn_fact(fact)
    except Exception as e:
        _log(agent_name, "learn_fact_error", str(e)[:200])


# ── Chronicle recording ──────────────────────────────────────────────────

def record(agent_name: str, url: str, context: str) -> None:
    """Index a URL and its content to Chronicle. Makes content searchable by all agents."""
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        agent.record_in_chronicle(url=url, context=context, source=agent_name)
    except Exception as e:
        _log(agent_name, "record_error", str(e)[:200])


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


# ── Shared learning ──────────────────────────────────────────────────────

def learn(agent_name: str, query: str, result: str,
          source_type: str = "web_verified", confidence: float = 0.85,
          urls: list = None) -> bool:
    """
    Write a result to unified cross-agent memory. All 21 agents share this.
    MemoryGuard enforces: source must be web_verified or chronicle, confidence >= 0.75.
    Returns True if persisted, False if blocked by guard.
    """
    try:
        from shared.memory_guard import sanitize_memory_write
        check = sanitize_memory_write(
            agent_name, result[:100], source_type, confidence
        )
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


def _extract_location_helpers(query: str):
    """Extract city and state from a query for geographic filtering.
    Returns (city, state_code) or (None, None) if no location detected."""
    import re
    _STATE_CODES = {
        "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN",
        "IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV",
        "NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN",
        "TX","UT","VT","VA","WA","WV","WI","WY","DC","PR"
    }
    _STATE_NAMES = {
        "alabama":"AL","alaska":"AK","arizona":"AZ","arkansas":"AR",
        "california":"CA","colorado":"CO","connecticut":"CT","delaware":"DE",
        "florida":"FL","georgia":"GA","hawaii":"HI","idaho":"ID",
        "illinois":"IL","indiana":"IN","iowa":"IA","kansas":"KS",
        "kentucky":"KY","louisiana":"LA","maine":"ME","maryland":"MD",
        "massachusetts":"MA","michigan":"MI","minnesota":"MN",
        "mississippi":"MS","missouri":"MO","montana":"MT","nebraska":"NE",
        "nevada":"NV","new hampshire":"NH","new jersey":"NJ",
        "new mexico":"NM","new york":"NY","north carolina":"NC",
        "north dakota":"ND","ohio":"OH","oklahoma":"OK","oregon":"OR",
        "pennsylvania":"PA","rhode island":"RI","south carolina":"SC",
        "south dakota":"SD","tennessee":"TN","texas":"TX","utah":"UT",
        "vermont":"VT","virginia":"VA","washington":"WA",
        "west virginia":"WV","wisconsin":"WI","wyoming":"WY",
        "district of columbia":"DC","puerto rico":"PR",
    }
    # Strip leading command prefix like /court, /jurisdiction, /law
    clean = re.sub(r'^/[a-z_]+\s+', '', query.strip(), count=1)
    # Strip bare command words: "court Denver CO" -> "Denver CO"
    _CMD_WORDS = {"court", "jurisdiction", "law", "state", "federal", "police", "hospital", "library", "detention", "judge", "statute", "docket", "precedent"}
    _parts = clean.strip().split()
    if _parts and _parts[0].lower() in _CMD_WORDS:
        clean = " ".join(_parts[1:])
    # Pattern: "City, ST" or "City ST" at end
    match = re.search(r"([A-Za-z\s]+),?\s+([A-Z]{2})\s*$", clean.strip())
    if match:
        city = match.group(1).strip()
        state = match.group(2).upper()
        if state in _STATE_CODES:
            return city, state
    # Pattern: standalone 2-letter code anywhere
    words = clean.upper().split()
    for w in words:
        if w in _STATE_CODES:
            # Find what comes before the state code as potential city
            idx = words.index(w)
            if idx > 0:
                return words[idx-1].title(), w
            return None, w
    # Pattern: full state name
    clean_lower = clean.lower()
    for name, code in sorted(_STATE_NAMES.items(), key=lambda x: -len(x[0])):
        if name in clean_lower:
            return None, code
    return None, None


def recall_memory(agent_name: str, query: str, limit: int = 5) -> list:
    """Search unified memory for prior results across all agents.
    Applies geographic filtering when city/state detected in query."""
    try:
        from shared.memory.unified_memory import UnifiedMemory
        mem = UnifiedMemory()
        
        city, state = _extract_location_helpers(query)
        
        terms = query.lower().split()
        matches = []
        for fact in mem._facts:
            fact_text = (
                fact.get("fact", "") + " " + fact.get("query", "")
            ).lower()
            score = sum(1 for t in terms if t in fact_text)
            if score > 0:
                geo_bonus = 0
                if state and state.lower() in fact_text:
                    geo_bonus = 3
                if city and city.lower() in fact_text:
                    geo_bonus += 2
                matches.append((score + geo_bonus, fact))
        
        matches.sort(key=lambda x: (-x[0], -x[1].get("confidence", 0)))
        return [m[1] for m in matches[:limit]]
    except Exception as e:
        _log(agent_name, "recall_error", str(e)[:200])
    return []


def smart_llm(agent_name: str, prompt: str, timeout: int = 120) -> str:
    """Full truth resolver pipeline with fallback to standard llm()."""
    try:
        from shared.base_agent import BaseAgent
        agent = BaseAgent(agent_name)
        return agent.smart_ask(prompt)
    except Exception as e:
        _log(agent_name, "smart_llm_fallback", str(e)[:100])
        return llm(agent_name, prompt, timeout=timeout)


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