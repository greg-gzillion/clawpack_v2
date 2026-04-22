#!/usr/bin/env python3
"""LawClaw - Pure Logic Legal Agent with Dynamic Command Loading"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import command registry
from commands import COMMAND_REGISTRY, get_command_help, load_all_commands

# A2A Collaboration Layer
try:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from agents.shared.a2a_client import A2AClient
    a2a_client = A2AClient()
except Exception as e:
    a2a_client = None
    print(f"⚠ A2A unavailable: {e}")


# Import utilities
try:
    from cli.parser import parse_command
except ImportError:
    def parse_command(cmd):
        parts = cmd.strip().split(' ', 1)
        return parts[0].lower(), parts[1] if len(parts) > 1 else ""

try:
    from utils.display import display
except ImportError:
    class Display:
        def banner(self, t, i=""): 
            print(f"\n{'='*70}\n{t}\n{'='*70}")
    display = Display()

class LawClaw:
    def __init__(self):
        # Load all commands dynamically
        print("Loading commands...")
        load_all_commands()
        self.commands = COMMAND_REGISTRY
        self.stats = {"queries": 0}
        self.print_welcome()
    
    def print_welcome(self):
        print("\n" + "="*70)
        print("⚖️ LAWCLAW - AI Legal Research".center(70))
        print("="*70)
        print("Connected to WebClaw: 31,686+ legal files")
        print(f"Commands loaded: {len(self.commands)}")
        print("\nType /help for commands, /quit to exit")
    
    def run(self):
        while True:
            try:
                cmd_input = input("\n⚖️ lawclaw> ").strip()
                if not cmd_input:
                    continue
                
                command, args = parse_command(cmd_input)
                
                if command == "/quit":
                    print("Goodbye!")
                    break
                elif command == "/help":
                    print(get_command_help())
                elif command == "/stats":
                    self.show_stats()
                elif command in self.commands:
                    self.stats["queries"] += 1
                    try:
                        result = self.commands[command](args)
                        if result:
                            print(result)
                    except Exception as e:
                        print(f"Error executing command: {e}")
                else:
                    print(f"Unknown command: {command}")
                    print("Type /help for available commands")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def show_stats(self):
        print("\n📊 LAWCLAW STATS")
        print("="*40)
        print(f"Queries this session: {self.stats['queries']}")
        print(f"Commands loaded: {len(self.commands)}")
        print(f"WebClaw references: 31,686+ legal files")
        print("LLM Available: Yes")
        print("A2A Server: http://127.0.0.1:8766")
        print("="*40)

if __name__ == "__main__":
    agent = LawClaw()
    agent.run()

