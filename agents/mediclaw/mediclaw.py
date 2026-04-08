#!/usr/bin/env python3
"""mediclaw.py - Medical Information Agent"""

from cli import parse_command
from commands import test_command, help_command, quit_command, search_command, symptoms_command, conditions_command

class mediclaw:
    def __init__(self):
        self.commands = {
            "/test": test_command,
            "/help": help_command,
            "/quit": quit_command,
            "/search": search_command,
            "/symptoms": symptoms_command,
            "/conditions": conditions_command,
        }
        self.print_welcome()
    
    def print_welcome(self):
        from core.data import get_data_path
        print("\n" + "="*70)
        print("🏥 MEDICLAW - Medical Information Agent")
        print("="*70)
        print(f"Data: {get_data_path()}")
        print("\nCOMMANDS:")
        print("  /test              - Test agent")
        print("  /search [term]     - Search medical references")
        print("  /symptoms [cond]   - Find symptoms for condition")
        print("  /conditions [symp] - Find conditions for symptom")
        print("  /help              - Show help")
        print("  /quit              - Exit")
        print("="*70)
    
    def run(self):
        self.print_welcome()
        while True:
            try:
                cmd = input("\nmediclaw> ").strip()
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
    agent = mediclaw()
    agent.run()