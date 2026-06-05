"""Share content to Chronicle"""
from pathlib import Path

name = "/share"

def run(args, agent=None):
    if not args:
        return "Usage: /share <content>"
    try:
        from agents.webclaw.core.chronicle_ledger import get_chronicle
        chronicle = get_chronicle()
        rid = chronicle.record_fetch(
            url="shared://webclaw",
            context=args,
            source="webclaw_share",
        )
        return f"Shared to Chronicle (id={rid})" if rid else "Failed to share"
    except Exception as e:
        return f"Share error: {e}"
