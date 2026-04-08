#!/usr/bin/env python3
"""
WEBCLAW - Web Research & Security Analysis System
Modular commands with shared memory and cross-agent learning
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from cli import parse_command
from commands import (cache_stats_command, 
    stats_command, list_command, search_command,
    browse_command, fetch_command, llm_command,
    help_command, share_command, recall_command, quit_command
)
from utils import display

class WebClaw:
    def __init__(self):
        self.running = True
        self.commands = {
            "/stats": stats_command,
            "/list": list_command,
            "/search": search_command,
            "/browse": browse_command,
            "/fetch": fetch_command,
            "/llm": llm_command,
            "/share": share_command,
            "/recall": recall_command,
            "/help": help_command, "/cache": cache_stats_command,
            "/quit": quit_command,
            "/exit": quit_command,
        }

    def run(self):
        help_command()

        while self.running:
            try:
                user_input = input("\n🌐 webclaw> ").strip()

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
    app = WebClaw()
    app.run()


