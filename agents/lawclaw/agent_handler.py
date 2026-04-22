"""A2A Handler for LawClaw"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def process_task(task: str, agent: str = None):
    """Route A2A task to appropriate command"""
    task = task.strip()
    
    # Parse command (e.g., "/court denver county")
    parts = task.split(maxsplit=1)
    cmd = parts[0].lower() if parts else ""
    args = parts[1] if len(parts) > 1 else ""
    
    # Import commands dynamically
    try:
        if cmd == "/court":
            from commands.court import run
            result = run(args)
        elif cmd == "/search":
            from commands.search import run
            result = run(args)
        elif cmd == "/ask":
            from commands.ask import run
            result = run(args)
        elif cmd == "/law":
            from commands.law import run
            result = run(args)
        elif cmd == "/statute":
            from commands.statute import run
            result = run(args)
        elif cmd == "/list":
            from commands.list import run
            result = run(args)
        elif cmd == "/help":
            from commands import get_command_help
            result = get_command_help()
        else:
            # Try to load dynamically
            cmd_name = cmd.lstrip('/')
            try:
                module = __import__(f"commands.{cmd_name}", fromlist=['run'])
                result = module.run(args)
            except:
                result = f"Unknown command: {cmd}"
        
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "result": str(e)}
