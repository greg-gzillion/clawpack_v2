#!/usr/bin/env python3
"""Mathematicaclaw - Math Agent with Plotting"""
import sys
from pathlib import Path

def process_command(cmd: str) -> str:
    cmd = cmd.strip()
    parts = cmd.split(maxsplit=1)
    command = parts[0].lower() if parts else ""
    args = parts[1] if len(parts) > 1 else ""
    
    # Try to load command from commands folder
    cmd_file = Path(__file__).parent / "commands" / f"{command}.py"
    if cmd_file.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location(command, cmd_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, 'run'):
            return module.run(args)
    
    # Built-in commands fallback
    if command == "plot":
        from commands.plot import run
        return run(args)
    elif command == "add":
        from commands.add import run
        return run(args)
    elif command == "solve":
        from commands.solve import run
        return run(args)
    elif command == "/help":
        return """
📐 MATHEMATICACLAW

Commands:
  add 2 3 4     - Add numbers
  plot x**2     - Plot function (opens window)
  solve x**2=16 - Solve equation
  /help         - This help
  /quit         - Exit
"""
    elif command == "/quit":
        return "QUIT"
    else:
        return f"Unknown: {command}. Try add, plot, or solve"

def main():
    if len(sys.argv) > 1:
        print(process_command(' '.join(sys.argv[1:])))
        return
    
    print("\n📐 MATHEMATICACLAW - Math Agent")
    print("Type /help for commands, /quit to exit")
    
    while True:
        try:
            cmd = input("\nmath> ").strip()
            if cmd == "/quit":
                break
            if cmd:
                result = process_command(cmd)
                print(result)
                if result == "QUIT":
                    break
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
