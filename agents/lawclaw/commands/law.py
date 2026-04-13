"""law command - Legal research"""

name = "/law"

def run(args):
    if not args:
        return "Usage: /law [topic]"
    return f"Legal research: {args}\n[WebClaw integration ready]"
