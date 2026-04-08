#!/usr/bin/env python3
"""docuclaw.py - Document Creation Agent"""

from cli import parse_command
from commands import test_command, help_command, quit_command

class docuclaw:
    def __init__(self):
        self.commands = {
            "/test": test_command,
            "/help": help_command,
            "/quit": quit_command,
        }
        self.print_welcome()
    
    def print_welcome(self):
        from core.data import get_data_path
        print("\n" + "="*70)
        print("📄 DOCUCLAW - Document Creation Agent")
        print("="*70)
        print(f"Data: {get_data_path()}")
        print("\nCOMMANDS:")
        print("  /test              - Test agent")
        print("  /help              - Show help")
        print("  /quit              - Exit")
        print("="*70)
    
    def run(self):
        self.print_welcome()
        while True:
            try:
                cmd = input("\ndocuclaw> ").strip()
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
    agent = docuclaw()
    agent.run()