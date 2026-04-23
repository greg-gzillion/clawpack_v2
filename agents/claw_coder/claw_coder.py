#!/usr/bin/env python3
"""claw_coder - Modular AI Programming Assistant"""
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

def process_command(cmd: str) -> str:
    cmd = cmd.strip()
    
    if cmd.startswith("code "):
        from commands.code import run
        return run(cmd[5:].strip())
    elif cmd.startswith("explain "):
        from commands.explain import run
        return run(cmd[8:].strip())
    elif cmd.startswith("debug "):
        from commands.debug import run
        return run(cmd[6:].strip())
    elif cmd.startswith("review "):
        from commands.review import run
        return run(cmd[7:].strip())
    elif cmd.startswith("tutorial "):
        from commands.tutorial import run
        return run(cmd[9:].strip())
    elif cmd == "/help":
        return """
💻 CLAW_CODER - AI Programming Assistant

Commands:
  code <task>           - Generate code
  explain <code>        - Explain code
  debug <code> [error]  - Debug code (use | for error)
  review <code>         - Code review
  tutorial <topic> [lang] [level] - Programming tutorial
  /help                 - This help
  /quit                 - Exit

Examples:
  code 'read CSV file'
  explain 'def fib(n): return n if n<2 else fib(n-1)+fib(n-2)'
  tutorial lists python beginner
"""
    elif cmd == "/quit":
        return "QUIT"
    else:
        return f"Unknown: {cmd}. Type /help"

def main():
    if len(sys.argv) > 1:
        print(process_command(' '.join(sys.argv[1:])))
        return
    
    print("\n💻 CLAW_CODER - AI Programming Assistant")
    print("Type /help for commands, /quit to exit")
    
    while True:
        try:
            cmd = input("\nclaw_coder> ").strip()
            if cmd == "/quit":
                break
            if cmd:
                result = process_command(cmd)
                print(result)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()

