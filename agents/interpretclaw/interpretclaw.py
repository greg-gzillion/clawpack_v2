#!/usr/bin/env python3
"""INTERPRETCLAW - Human Language Translation Hub"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

class InterpretClaw:
    def __init__(self):
        self.commands = {}
        self._load_commands()
    
    def _load_commands(self):
        cmds_path = Path(__file__).parent / "commands"
        for py_file in cmds_path.glob("*.py"):
            if py_file.name.startswith("__"):
                continue
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location(py_file.stem, py_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'name') and hasattr(module, 'run'):
                    self.commands[module.name] = module.run
            except: pass
    
    def run(self):
        print("\n" + "█"*70)
        print("█" + " "*68 + "█")
        print("█" + " "*12 + "🌐 INTERPRETCLAW - LANGUAGE HUB 🌐" + " "*12 + "█")
        print("█" + " "*68 + "█")
        print("█"*70)
        
        if "/help" in self.commands:
            self.commands["/help"](None)
        
        while True:
            try:
                cmd = input("\n🌐 interpretclaw> ").strip()
                if not cmd:
                    continue
                if cmd == "/quit":
                    print("Goodbye!")
                    break
                parts = cmd.split(" ", 1)
                command = parts[0]
                args = parts[1] if len(parts) > 1 else ""
                if command in self.commands:
                    self.commands[command](args)
                else:
                    print(f"Unknown: {command}. Type /help")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break

if __name__ == "__main__":
    InterpretClaw().run()
