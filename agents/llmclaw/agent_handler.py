"""A2A Handler for LLMClaw"""
import sys
import os
from pathlib import Path

LLMCLAW_DIR = Path(__file__).parent
os.chdir(str(LLMCLAW_DIR))
sys.path.insert(0, str(LLMCLAW_DIR.parent.parent))

def process_task(task: str, agent: str = None):
    os.chdir(str(LLMCLAW_DIR))
    task = task.strip()
    parts = task.split(maxsplit=1)
    cmd = parts[0].lower() if parts else ""
    args = parts[1] if len(parts) > 1 else ""
    
    try:
        if cmd == "/llm":
            from commands.llm import run  # CHANGED from ask
            result = run(args)
        elif cmd == "/list":
            from commands.list import run
            result = run(args)
        elif cmd == "/use":
            from commands.use import run
            result = run(args)
        elif cmd == "/normal":
            from commands.normal import run
            result = run(args)
        elif cmd == "/obliterated":
            from commands.obliterated import run
            result = run(args)
        else:
            result = f"Unknown command: {cmd}"
        
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "result": str(e)}
