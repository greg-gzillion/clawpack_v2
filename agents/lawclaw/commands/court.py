"""court command - County court info"""

name = "/court"

def run(args):
    if not args:
        return "Usage: /court [state] [county]"
    return f"Court info for: {args}\n[WebClaw integration ready]"
