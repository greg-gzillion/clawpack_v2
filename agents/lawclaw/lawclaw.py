#!/usr/bin/env python3
"""LAWCLAW - Modular Judicial Research System"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from core import Display
from commands import get_all_commands

class LawClaw:
    def __init__(self):
        self.commands = get_all_commands()
    
    def run(self):
        Display.banner()
        Display.categories()
        Display.commands(list(self.commands.keys()))
        
        while True:
            try:
                cmd = input("\n⚖️ lawclaw> ").strip()
                if not cmd:
                    continue
                if cmd in ['/quit', '/exit']:
                    print("Goodbye!")
                    break
                parts = cmd.split(' ', 1)
                if parts[0] in self.commands:
                    self.commands[parts[0]](parts[1] if len(parts) > 1 else "")
                else:
                    print(f"Unknown: {parts[0]}. Type /help")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break

if __name__ == "__main__":
    LawClaw().run()
