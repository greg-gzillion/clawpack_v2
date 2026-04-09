#!/usr/bin/env python3
"""DOCUCLAW - Document Processing Agent with Translation"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

class DocuClaw:
    def __init__(self):
        self.commands = {}
        self._load_commands()
    
    def _load_commands(self):
        cmds_path = Path(__file__).parent / "commands"
        if not cmds_path.exists():
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
                    self.commands[module.name] = module.run
            except Exception as e:
                print(f"Error loading {py_file.name}: {e}")
    
    def run(self):
        print("\n" + "="*60)
        print("📝 DOCUCLAW - Document Processing Agent".center(60))
        print("="*60)
        print("Translate • Review • Convert • Export".center(60))
        print("="*60)
        
        print("\n📝 COMMANDS:")
        print("  /translate <file> to <lang>  - Translate document")
        print("  /review [file]               - Review document (pop-up)")
        print("  /list                        - List documents")
        print("  /help                        - Show commands")
        print("  /quit                        - Exit")
        
        print("\n📄 EXAMPLE:")
        print("  /translate report.txt to es")
        print("  /review report_es.txt")
        
        while True:
            try:
                cmd = input("\n📝 Docu > ").strip()
                if not cmd:
                    continue
                
                if cmd == "/quit":
                    print("Goodbye!")
                    break
                elif cmd == "/help":
                    self._show_help()
                elif cmd == "/list":
                    self._list_documents()
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
                print("\nGoodbye!")
                break
    
    def _show_help(self):
        print("\n📝 Available commands:")
        for name in sorted(self.commands.keys()):
            print(f"  /{name} - {self.commands[name].__doc__ or 'No description'}")
    
    def _list_documents(self):
        docs = list(Path(".").glob("*.txt")) + list(Path(".").glob("*.md")) + list(Path(".").glob("*.docx"))
        if docs:
            print("\n📁 Documents:")
            for d in docs[:20]:
                print(f"  • {d.name}")
        else:
            print("\n📁 No documents found.")

if __name__ == "__main__":
    DocuClaw().run()
