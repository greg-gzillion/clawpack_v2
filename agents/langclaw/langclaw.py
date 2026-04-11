#!/usr/bin/env python3
"""Langclaw - AI Language Teaching Agent with Chronicle Integration"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def process_command(cmd: str) -> str:
    cmd = cmd.strip()
    
    if cmd.startswith("/lesson "):
        from commands.lesson import run
        return run(cmd[8:].strip())
    elif cmd.startswith("/practice "):
        from commands.practice import run
        return run(cmd[10:].strip())
    elif cmd.startswith("/vocab "):
        from commands.vocab import run
        return run(cmd[7:].strip())
    elif cmd.startswith("/conversation "):
        from commands.conversation import run
        return run(cmd[14:].strip())
    elif cmd.startswith("/grammar "):
        # Grammar command coming soon
        return "Grammar lessons coming soon!"
    elif cmd == "/help":
        return """
📚 LANGCLAW - AI Language Teaching Agent

Commands:
  /lesson <lang> <topic> [level]  - Structured lesson (beginner/intermediate/advanced)
  /practice <lang> [topic]        - Practice exercises
  /vocab <lang> <word>            - Detailed vocabulary with examples
  /conversation <lang> <scenario> - Conversation practice
  speak <text>                    - Pronunciation practice
  /listen                         - Speech recognition
  /help                           - This help
  /quit                           - Exit

Examples:
  /lesson spanish greetings beginner
  /practice french
  /vocab german hallo
  /conversation spanish restaurant
  speak hello world
"""
    elif cmd.startswith("speak "):
        import subprocess
        try:
            subprocess.run(["espeak", cmd[6:]], capture_output=True, timeout=10)
            return f"🔊 Speaking: {cmd[6:]}"
        except:
            return "🔊 espeak not installed"
    elif cmd == "/listen":
        return "🎤 Say something in the target language..."
    elif cmd == "/quit":
        return "QUIT"
    else:
        from core.llm_manager import LLMManager
        llm = LLMManager()
        return llm.chat_sync(f"As a language teacher, answer: {cmd}")

def main():
    if len(sys.argv) > 1:
        print(process_command(' '.join(sys.argv[1:])))
        return
    
    print("\n📚 LANGCLAW - AI Language Teaching Agent")
    print("Powered by Groq LLM + Chronicle Index")
    print("Type /help for commands, /quit to exit")
    
    while True:
        try:
            cmd = input("\nlangclaw> ").strip()
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
