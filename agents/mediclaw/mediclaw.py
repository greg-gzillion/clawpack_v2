#!/usr/bin/env python3
"""Mediclaw - Medical Information Agent"""
import sys
from pathlib import Path

def process_command(cmd: str) -> str:
    cmd = cmd.strip()
    
    if cmd.startswith("/med "):
        topic = cmd[5:].strip()
        from commands.med import run
        return run(topic)
    elif cmd == "/help":
        return """
🏥 MEDICLAW - Medical Information Agent

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
    
    print("\n🏥 MEDICLAW - Medical Information Agent")
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
