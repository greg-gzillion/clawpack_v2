def court_command(args):
    if not args:
        return "Usage: /court <state> <county>"
    parts = args.split()
    if len(parts) < 2:
        return "Usage: /court <state> <county>"
    return f"Court info for {parts[1]} County, {parts[0].upper()}"
