"""browse command - Browse state courts"""

name = "/browse"

def run(args):
    if not args:
        return "Usage: /browse [state]"
    return f"Browsing courts for: {args}\n[WebClaw integration ready]"
