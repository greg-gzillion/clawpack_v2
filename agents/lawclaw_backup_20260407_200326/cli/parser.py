def parse_command(cmd):
    if not cmd:
        return None, None
    parts = cmd.split(' ', 1)
    return parts[0].lower(), parts[1] if len(parts) > 1 else ""
