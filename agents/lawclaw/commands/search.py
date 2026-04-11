def search_command(args):
    if not args:
        return "Usage: /search <query>"
    return f"Searching for: {args}\nUse WebClaw to fetch results"
