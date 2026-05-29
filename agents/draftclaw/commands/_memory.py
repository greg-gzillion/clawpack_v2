"""draftclaw shared memory helper — constitutional cross-command learning."""
from datetime import datetime, timezone
from typing import Optional

def _log(event, detail=""):
    try:
        from agents.webclaw.core.chronicle_ledger import log_event
        log_event(agent="draftclaw", event=event, detail=str(detail)[:500])
    except Exception: pass

def recall(query: str, limit: int = 5) -> list:
    try:
        from shared.memory.unified_memory import UnifiedMemory
        mem = UnifiedMemory()
        terms = query.lower().split()
        matches = []
        for fact in mem._facts:
            fact_text = (fact.get("fact", "") + " " + fact.get("query", "")).lower()
            score = sum(1 for t in terms if t in fact_text)
            if score > 0: matches.append((score, fact))
        matches.sort(key=lambda x: (-x[0], -x[1].get("confidence", 0)))
        return [m[1] for m in matches[:limit]]
    except Exception as e: _log("memory_recall_error", str(e)[:200])
    return []

def remember(command: str, query: str, result_summary: str,
             source_type: str, confidence: float,
             urls: Optional[list] = None, metadata: Optional[dict] = None) -> bool:
    try:
        from shared.memory_guard import sanitize_memory_write
        check = sanitize_memory_write("draftclaw", result_summary[:100], source_type, confidence)
        if not check.get("allowed"): return False
        from shared.memory.unified_memory import UnifiedMemory
        mem = UnifiedMemory()
        fact = {"agent": "draftclaw", "command": command, "query": query,
                "fact": result_summary[:500], "source_type": source_type,
                "confidence": confidence, "urls": urls or [], "metadata": metadata or {},
                "timestamp": datetime.now(timezone.utc).isoformat()}
        mem._facts.append(fact)
        for word in query.lower().split():
            if len(word) > 3:
                if word not in mem._index: mem._index[word] = []
                mem._index[word].append(len(mem._facts) - 1)
        mem._save_index()
        return True
    except Exception as e: _log("memory_write_error", str(e)[:200])
    return False

def show_prior(query: str, out: list) -> list:
    prior = recall(query, limit=3)
    if prior:
        out.append(f"  [MEMORY] {len(prior)} related prior search(es) found:")
        for p in prior[:2]:
            cmd = p.get("command", "unknown"); ts = p.get("timestamp", "")[:10]
            summary = p.get("fact", "")[:80]
            out.append(f"    {cmd} [{ts}]: {summary}...")
    return prior
