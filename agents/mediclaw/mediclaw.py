#!/usr/bin/env python3
"""Mediclaw - Medical Information Agent"""
import sys
from pathlib import Path

# A2A Collaboration Layer
try:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from shared.a2a_client import A2AClient
    a2a_client = A2AClient()
except Exception as e:
    a2a_client = None
    print(f"⚠ A2A unavailable: {e}")


def process_command(cmd: str) -> str:
    cmd = cmd.strip()
    
    if cmd.startswith("/med "):
        topic = cmd[5:].strip()
        from commands.med import run
        return run(topic)
    elif cmd == "/help":
        return """
ðŸ¥ MEDICLAW - Medical Information Agent

Commands:
  /med <condition>   - Get medical information
  /help              - Show this help
  /quit              - Exit
"""
    elif cmd == "/quit":
        return "QUIT"
    else:
        return f"Unknown: {cmd}. Type /help"

def main():
    if len(sys.argv) > 1:
        print(process_command(' '.join(sys.argv[1:])))
        return
    
    print("\nðŸ¥ MEDICLAW - Medical Information Agent")
    print("Type /help for commands, /quit to exit")
    
    while True:
        try:
            cmd = input("\nmediclaw> ").strip()
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

