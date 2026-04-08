#!/usr/bin/env python3
"""
LAWCLAW - Judicial Research & Court Information System
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from cli import parse_command
from commands import (
    stats_command, list_command, search_command,
    browse_command, court_command, llm_command,
    help_command, quit_command
)
from utils import display

class LawClaw:
    def __init__(self):
        self.running = True
        self.commands = {
            "/stats": stats_command,
            "/list": list_command,
            "/search": search_command,
            "/browse": browse_command,
            "/court": court_command,
            "/llm": llm_command,
            "/help": help_command,
            "/quit": quit_command,
            "/exit": quit_command,
        }

    def run(self):
        help_command()
        
        while self.running:
            try:
                user_input = input("\n⚖️ lawclaw> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.startswith('/'):
                    cmd, args = parse_command(user_input)
                    
                    if cmd in self.commands:
                        result = self.commands[cmd](args)
                        if result is True:
                            self.running = False
                            break
                    else:
                        print(f"Unknown command: {cmd}")
                        print("Type /help for available commands")
                else:
                    llm_command(user_input)
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    app = LawClaw()
    app.run()
