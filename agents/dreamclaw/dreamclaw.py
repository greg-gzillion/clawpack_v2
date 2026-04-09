#!/usr/bin/env python3
"""DREAMCLAW - AI Image Generation Agent"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

class DreamClaw:
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
            except Exception as e:
                print(f"Error loading {py_file.name}: {e}")
    
    def run(self):
        print("\n" + "="*60)
        print("🎨 DREAMCLAW - AI Image Generation".center(60))
        print("="*60)
        print("DALL-E • Stable Diffusion • Flux".center(60))
        print("="*60)
        
        print("\n🎨 COMMANDS:")
        print("  /dream <prompt>           - Generate image")
        print("  /imagine <prompt>         - Same as dream")
        print("  /style <name>             - Set style (realistic, anime, etc)")
        print("  /list                     - List generated images")
        print("  /help                     - Show commands")
        print("  /quit                     - Exit")
        
        print("\n🖼️ EXAMPLE:")
        print("  /dream a lobster teaching Spanish in a classroom")
        print("  /style anime")
        
        while True:
            try:
                cmd = input("\n🎨 Dream > ").strip()
                if not cmd:
                    continue
                
                if cmd == "/quit":
                    print("Dream on!")
                    break
                elif cmd == "/help":
                    self._show_help()
                elif cmd.startswith("/"):
                    parts = cmd[1:].split(maxsplit=1)
                    cmd_name = parts[0]
                    args = parts[1] if len(parts) > 1 else ""
                    
                    if cmd_name in self.commands:
                        result = self.commands[cmd_name](args)
                        print(result)
                    else:
                        print(f"Unknown: /{cmd_name}")
                else:
                    print("Commands start with / (type /help)")
                    
            except KeyboardInterrupt:
                print("\nDream on!")
                break
    
    def _show_help(self):
        print("\n🎨 Available commands:")
        for name in sorted(self.commands.keys()):
            print(f"  /{name} - {self.commands[name].__doc__ or 'No description'}")

if __name__ == "__main__":
    DreamClaw().run()
