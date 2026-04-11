def browse_command(args):
    if not args:
        return "Usage: /browse <state>"
    return f"Browsing courts in {args.upper()}"
