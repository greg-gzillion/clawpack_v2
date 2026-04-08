#!/usr/bin/env python3
"""WebClaw - AI Agent with API Server for other agents"""

import sys
import os
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# Start API server in background thread
from api_server import app as api_app
import threading

def run_api():
    """Run Flask API server in background"""
    print("🌐 WebClaw API Server starting on port 5000...")
    api_app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# Start API server in background thread
api_thread = threading.Thread(target=run_api, daemon=True)
api_thread.start()

# Now run the interactive REPL
from cli import parse_command
from commands import (
    stats_command, list_command, search_command,
    browse_command, fetch_command, llm_command,
    help_command, share_command, recall_command, quit_command
)

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
            "/help": help_command,
            "/quit": quit_command,
            "/exit": quit_command,
        }
        self.print_banner()

    def print_banner(self):
        print("\n" + "█"*70)
        print("█" + " "*68 + "█")
        print("█" + " "*15 + "🌐 WEBCLAW - WEB RESEARCH AGENT 🌐" + " "*15 + "█")
        print("█" + " "*68 + "█")
        print("█"*70)
        help_command()

    def run(self):
        while self.running:
            try:
                cmd = input("\n🌐 webclaw> ").strip()
                if not cmd:
                    continue

                if cmd.startswith('/'):
                    cmd_name, args = parse_command(cmd)
                    if cmd_name in self.commands:
                        result = self.commands[cmd_name](args)
                        if result is True:
                            self.running = False
                            break
                    else:
                        print(f"Unknown: {cmd_name}. Type /help")
                else:
                    llm_command(cmd)

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    agent = WebClaw()
    agent.run()
