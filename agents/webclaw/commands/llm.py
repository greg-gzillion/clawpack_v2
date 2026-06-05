"""LLM command with Chronicle-backed memory"""
from pathlib import Path

WEB_REFS = Path(__file__).resolve().parent.parent / "references"
name = "/llm"

def run(args, agent=None):
    if not args:
        return "Usage: /llm <query>"
    
    # Gather reference context
    context_parts = []
    if WEB_REFS.exists():
        for cat in sorted(WEB_REFS.iterdir()):
            if cat.is_dir():
                context_parts.append(f"[{cat.name}] references available")
    
    # Search Chronicle for relevant history
    try:
        from agents.webclaw.core.chronicle_ledger import get_chronicle
        chronicle = get_chronicle()
        results = chronicle.recover_by_context(args, limit=5)
        if results:
            context_parts.append("[Chronicle]: " + str(len(results)) + " past results")
    except Exception:
        pass
    
    if agent:
        prompt = f"Query: {args}\n\nContext:\n" + "\n".join(context_parts)
        return agent.ask_llm(prompt)
    return "\n".join(context_parts)
