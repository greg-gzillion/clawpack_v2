#!/usr/bin/env python3
"""polyclaw.py - Translation Agent"""

from cli import parse_command
from commands import test_command, help_command, quit_command, translate_command, languages_command

class polyclaw:
    def __init__(self):
        self.commands = {
            "/test": test_command,
            "/help": help_command,
            "/quit": quit_command,
            "/translate": translate_command,
            "/languages": languages_command,
        }
        self.print_welcome()
    
    def print_welcome(self):
        from core.data import get_data_path
        print("\n" + "="*70)
        print("🌐 POLYCLAW - Translation Agent")
        print("="*70)
        print(f"Data: {get_data_path()}")
        print("\nCOMMANDS:")
        print("  /test              - Test agent")
        print("  /translate [text]  - Translate text")
        print("  /languages         - List available languages")
        print("  /help              - Show help")
        print("  /quit              - Exit")
        print("="*70)
    
    def run(self):
        self.print_welcome()
        while True:
            try:
                cmd = input("\npolyclaw> ").strip()
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
    agent = polyclaw()
    agent.run()