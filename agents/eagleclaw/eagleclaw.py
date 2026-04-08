#!/usr/bin/env python3
"""eagleclaw.py - Main AI Assistant (API primary, local fallback)"""

from cli import parse_command
from commands import test_command, help_command, quit_command, ask_command, status_command, ollama_command, models_command

class eagleclaw:
    def __init__(self):
        self.commands = {
            "/test": test_command,
            "/help": help_command,
            "/quit": quit_command,
            "/ask": ask_command,
            "/status": status_command,
            "/ollama": ollama_command,
            "/models": models_command,
        }
        self.print_welcome()
    
    def print_welcome(self):
        from core.data import get_data_path
        print("\n" + "="*70)
        print("🦅 EAGLECLAW - Main AI Assistant")
        print("="*70)
        print(f"Data: {get_data_path()}")
        print("\nCOMMANDS:")
        print("  /ask [question]    - Ask anything (API primary, local fallback)")
        print("  /ask --legal       - Use legal-optimized model")
        print("  /ask --fast        - Use fast model")
        print("  /ask --local       - Force local LLM only")
        print("  /status            - Check API/local status")
        print("  /ollama [prompt]   - Direct local LLM")
        print("  /models            - List local models")
        print("  /test              - Test agent")
        print("  /help              - Show help")
        print("  /quit              - Exit")
        print("="*70)
    
    def run(self):
        self.print_welcome()
        while True:
            try:
                cmd = input("\neagleclaw> ").strip()
                if not cmd:
                    continue
                
                command, args = parse_command(cmd)
                if command in self.commands:
                    result = self.commands[command](args)
                    if result == "QUIT":
                        print("Goodbye!")
                        break
                else:
                    print(f"Unknown: {command}")
                        
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break

if __name__ == "__main__":
    agent = eagleclaw()
    agent.run()