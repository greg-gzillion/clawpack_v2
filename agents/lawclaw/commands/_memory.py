"""lawclaw shared memory helper — constitutional cross-command learning.

Import in any lawclaw command:
    from agents.lawclaw.commands._memory import recall, remember, show_prior

All writes pass through memory_guard (confidence >= 0.75, web_verified or chronicle only).
All reads return ranked results by truth priority.
"""
from datetime import datetime, timezone
from typing import Optional


def _log(event, detail=""):
    try:
        from agents.webclaw.core.chronicle_ledger import log_event
        log_event(agent="lawclaw", event=event, detail=str(detail)[:500])
    except Exception:
        pass


def _extract_location(query: str):
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


def recall(query: str, limit: int = 5) -> list:
    """Search unified memory for prior results related to this query.
    Applies geographic filtering when city/state detected in query."""
    try:
        from shared.memory.unified_memory import UnifiedMemory
        mem = UnifiedMemory()
        
        # Extract location for geographic filtering
        city, state = _extract_location(query)
        
        terms = query.lower().split()
        matches = []
        for fact in mem._facts:
            fact_text = (fact.get("fact", "") + " " + fact.get("query", "")).lower()
            score = sum(1 for t in terms if t in fact_text)
            if score > 0:
                # Geographic filter: if query has a location, prefer same-state results
                geo_bonus = 0
                if state and state.lower() in fact_text:
                    geo_bonus = 3  # Strong preference for same-state results
                if city and city.lower() in fact_text:
                    geo_bonus += 2  # Even stronger for same-city
                matches.append((score + geo_bonus, fact))
        
        # Sort by combined score (keyword + geographic), then confidence
        matches.sort(key=lambda x: (-x[0], -x[1].get("confidence", 0)))
        return [m[1] for m in matches[:limit]]
    except Exception as e:
        _log("memory_recall_error", str(e)[:200])
    return []


def remember(command: str, query: str, result_summary: str,
             source_type: str, confidence: float,
             urls: Optional[list] = None,
             metadata: Optional[dict] = None) -> bool:
    """Write a result to unified memory if it passes the memory guard."""
    try:
        from shared.memory_guard import sanitize_memory_write
        check = sanitize_memory_write("lawclaw", result_summary[:100], source_type, confidence)
        if not check.get("allowed"):
            return False

        from shared.memory.unified_memory import UnifiedMemory
        mem = UnifiedMemory()

        fact = {
            "agent": "lawclaw",
            "command": command,
            "query": query,
            "fact": result_summary[:500],
            "source_type": source_type,
            "confidence": confidence,
            "urls": urls or [],
            "metadata": metadata or {},
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
        _log("memory_write_error", str(e)[:200])
    return False
def remember_court(code: str, data: dict) -> bool:
    """Persist jurisdiction context for downstream agent use."""
    import json
    return remember(
        command="jurisdiction_lookup",
        query=f"court:{code}",
        result_summary=json.dumps(data),
        source_type="chronicle",
        confidence=0.95
    )


def recall_court(code: str) -> dict | None:
    """Retrieve stored court context for cross-agent delegation.
    
    Handles 2-character state codes that get filtered by the keyword index.
    recall() ignores words < 3 chars, so "MS", "VA", "TX" get dropped.
    """
    # Try exact match first
    matches = recall(f"court:{code}", limit=1)
    if matches:
        return matches[0]
    
    # If code ends with a 2-char state, search city name only
    parts = code.strip().split()
    if len(parts) >= 2 and len(parts[-1]) == 2:
        city_only = " ".join(parts[:-1])
        matches = recall(f"court:{city_only}", limit=3)
        if matches:
            return matches[0]
        # Broader search for any court entry matching this city
        matches = recall(city_only, limit=5)
        if matches:
            for m in matches:
                if "court:" in m.get("query", ""):
                    return m
    
    return None
def show_prior(query: str, out: list) -> list:
    """Check memory and append prior search notice to output list if found."""
    prior = recall(query, limit=3)
    if prior:
        out.append(f"  [MEMORY] {len(prior)} related prior search(es) found:")
        for p in prior[:2]:
            cmd = p.get("command", "unknown")
            ts = p.get("timestamp", "")[:10]
            summary = p.get("fact", "")[:80]
            out.append(f"    {cmd} [{ts}]: {summary}...")
    return prior
