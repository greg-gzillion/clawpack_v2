"""Recall from Chronicle memory"""
from pathlib import Path

name = "/recall"

def run(args, agent=None):
    if not args:
        return "Usage: /recall <query>"
    try:
        from agents.webclaw.core.chronicle_ledger import get_chronicle
        chronicle = get_chronicle()
        results = chronicle.recover_by_context(args, limit=10)
        if not results:
            return f"No results for {args!r}"
        lines = [f"Found {len(results)} results:"]
        for i, r in enumerate(results, 1):
            url = r.get("url", "")
            ctx = r.get("context", "")[:200]
            lines.append(f"{i}. {url}")
            if ctx:
                lines.append(f"   {ctx}")
        return "\n".join(lines)
    except Exception as e:
        return f"Recall error: {e}"
