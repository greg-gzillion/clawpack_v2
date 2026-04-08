"""Command parser for LawClaw"""

def parse_command(cmd_input: str):
    """Parse command input into command and args"""
    if not cmd_input:
        return None, None
    
    parts = cmd_input.strip().split(' ', 1)
    command = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""
    
    return command, args
