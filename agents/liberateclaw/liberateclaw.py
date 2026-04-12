#!/usr/bin/env python3
"""Liberateclaw - Model Liberation Agent (Modular)"""

import sys
import io
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def process_command(cmd: str) -> str:
    """Process liberateclaw commands"""
    cmd = cmd.strip()

    # Check exact matches first
    if cmd == "/liberated":
        from commands.liberated import list_liberated
        return list_liberated()
    elif cmd == "/models":
        from commands.models import list_models
        return list_models()
    elif cmd == "/remote":
        from commands.remote import show_remote_help
        return show_remote_help()
    elif cmd == "/help":
        return get_help()
    elif cmd == "/quit":
        return "QUIT"
    
    # Check startswith matches (order matters - longer first)
    elif cmd.startswith("/remote-liberate"):
        from commands.remote import remote_liberate
        return remote_liberate(cmd[17:].strip())
    elif cmd.startswith("/liberate"):
        from commands.liberate import run_liberate
        return run_liberate(cmd[10:].strip())
    elif cmd.startswith("/obliterate"):
        from commands.obliterate import run_obliterate
        return run_obliterate(cmd[12:].strip())
    elif cmd.startswith("/use"):
        parts = cmd[5:].split(maxsplit=1)
        if len(parts) == 2:
            from commands.use import run_use
            return run_use(parts[0], parts[1])
        return "Usage: /use <model> <prompt>"
    else:
        return f"Unknown: {cmd}\n{get_help()}"

def get_help():
    return """
╔══════════════════════════════════════════════════════════════════╗
║  🔓 LIBERATECLAW - Model Liberation Agent (Modular)             ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  COMMANDS:                                                       ║
║    /liberate <model>     - Liberate model via Ollama            ║
║    /obliterate <model>   - OBLITERATUS (advanced liberation)    ║
║    /use <model> <prompt> - Use liberated model                 ║
║    /models               - List available models               ║
║    /liberated            - List liberated models               ║
║    /remote               - Remote liberation help              ║
║    /remote-liberate <cmd> - Liberate on remote GPU server      ║
║                                                                  ║
║  EXAMPLES:                                                       ║
║    /liberate llama3.2:3b                                        ║
║    /obliterate meta-llama/Llama-3.1-8B-Instruct                ║
║    /use llama3.2:3b "Explain AI"                               ║
║    /remote-liberate --user user --host 10.0.0.5 --model name   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""

def main():
    if len(sys.argv) > 1:
        print(process_command(' '.join(sys.argv[1:])))
        return

    print("\n🔓 LIBERATECLAW - Model Liberation Agent (Modular)")
    print("Type /help for commands, /quit to exit")

    while True:
        try:
            cmd = input("\nliberateclaw> ").strip()
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
