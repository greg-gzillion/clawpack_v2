"""Command parser for WebClaw"""

def parse_command(user_input: str):
    """Parse command and arguments"""
    parts = user_input.strip().split(' ', 1)
    cmd = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""
    return cmd, args
