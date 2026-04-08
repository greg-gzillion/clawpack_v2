#!/usr/bin/env python3
"""DocuClaw - Modular Document & Code Processor"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

class DocuClaw:
    def __init__(self):
        self.commands = {}
        self._load_commands()
    
    def _load_commands(self):
        """Load all command modules from commands/ folder"""
        cmds_path = Path(__file__).parent / "commands"
        
        if not cmds_path.exists():
            print(f"⚠️ Commands folder not found: {cmds_path}")
            return
        
        for py_file in cmds_path.glob("*.py"):
            if py_file.name.startswith("__"):
                continue
            
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location(py_file.stem, py_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, 'name') and hasattr(module, 'run'):
                    cmd_name = module.name
                    self.commands[cmd_name] = module.run
                    print(f"  Loaded: {cmd_name}")
            except Exception as e:
                print(f"  Error loading {py_file.name}: {e}")
        
        print(f"\n✅ Loaded {len(self.commands)} commands")
    
    def run(self):
        print("\n" + "█"*70)
        print("█" + " "*68 + "█")
        print("█" + " "*12 + "📄 DOCUCLAW - DOCUMENT & CODE PROCESSOR 📄" + " "*12 + "█")
        print("█" + " "*68 + "█")
        print("█"*70)
        
        # Show help
        if "/help" in self.commands:
            self.commands["/help"](None)
        
        while True:
            try:
                cmd_input = input("\n📄 docuclaw> ").strip()
                if not cmd_input:
                    continue
                
                if cmd_input in ['/quit', '/exit']:
                    print("Goodbye!")
                    break
                
                # Split command and args
                parts = cmd_input.split(' ', 1)
                cmd = parts[0]
                args = parts[1] if len(parts) > 1 else ""
                
                if cmd in self.commands:
                    self.commands[cmd](args)
                else:
                    print(f"❌ Unknown: {cmd}")
                    print("   Type /help for available commands")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    DocuClaw().run()
