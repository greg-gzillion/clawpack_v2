#!/usr/bin/env python3
"""Interpretclaw - Translation, Language Learning with Chronicle"""
import sys
from pathlib import Path

def process_command(cmd: str) -> str:
    cmd = cmd.strip()
    
    if cmd.startswith("translate "):
        from commands.translate import run
        return run(cmd[10:].strip())
    elif cmd.startswith("speak "):
        from commands.speak import run
        return run(cmd[6:].strip())
    elif cmd == "/listen":
        from commands.listen import run
        return run("")
    elif cmd.startswith("/lesson "):
        from commands.lesson import run
        return run(cmd[8:].strip())
    elif cmd.startswith("/vocab "):
        from commands.vocab import run
        return run(cmd[7:].strip())
    elif cmd == "/help":
        return """
🌐 INTERPRETCLAW - Translation & Language Learning

Commands:
  translate <text> to <lang>  - Translate text using LLM
  speak <text>                - Text-to-speech
  /listen                     - Speech-to-text
  /lesson <lang> <topic>      - Language lesson from references
  /vocab <lang> <word>        - Vocabulary lookup
  /help                       - This help
  /quit                       - Exit
"""
    elif cmd == "/quit":
        return "QUIT"
    else:
        return f"Unknown: {cmd}. Type /help"

def main():
    if len(sys.argv) > 1:
        print(process_command(' '.join(sys.argv[1:])))
        return
    
    print("\n🌐 INTERPRETCLAW - Translation & Language Learning Agent")
    print("Type /help for commands, /quit to exit")
    
    while True:
        try:
            cmd = input("\ninterpret> ").strip()
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

# Add to clawpack integration
def process_command(cmd, *args):
    """Simple command processor for clawpack"""
    if cmd == "translate":
        text = ' '.join(args[:-1]) if len(args) > 1 else ''
        lang = args[-1] if args else 'spanish'
        return f"Translating '{text}' to {lang}... (AI would do this)"
    elif cmd == "speak":
        return f"Speaking: {' '.join(args)}"
    else:
        return "InterpretClaw ready. Commands: translate, speak"
