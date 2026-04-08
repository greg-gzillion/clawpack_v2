#!/usr/bin/env python3
"""ClawCoder - Multi-language Code Generation Agent"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.orchestrator import LanguageOrchestrator
from core.memory import SharedMemory

class ClawCoder:
    def __init__(self):
        self.memory = SharedMemory()
        self.orchestrator = LanguageOrchestrator()
        self.running = True
    
    def run(self):
        self._print_welcome()
        
        while self.running:
            try:
                cmd = input("\n🔧 claw_coder> ").strip()
                if not cmd:
                    continue
                
                if cmd == "/quit" or cmd == "/exit":
                    print("Goodbye!")
                    break
                elif cmd == "/help":
                    self._print_help()
                elif cmd == "/languages":
                    self._list_languages()
                elif cmd.startswith("/generate"):
                    self._generate(cmd[9:].strip())
                elif cmd.startswith("/analyze"):
                    self._analyze(cmd[8:].strip())
                else:
                    print(f"Unknown: {cmd}. Type /help")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
    
    def _print_welcome(self):
        print("\n" + "█"*70)
        print("█" + " "*68 + "█")
        print("█" + " "*15 + "🔧 CLAWCODER - MULTI-LANGUAGE CODE AGENT 🔧" + " "*15 + "█")
        print("█" + " "*68 + "█")
        print("█"*70)
        self._print_help()
    
    def _print_help(self):
        print("\n" + "="*60)
        print("COMMANDS")
        print("="*60)
        print("  /languages          - List supported languages")
        print("  /generate <lang> <prompt> - Generate code")
        print("  /analyze <file>     - Analyze code file")
        print("  /help               - This menu")
        print("  /quit               - Exit")
        print("="*60)
        print(f"\n💡 Supported languages: {', '.join(self.orchestrator.list_languages())}")
    
    def _list_languages(self):
        print(f"\n📚 Supported languages:\n")
        for lang in sorted(self.orchestrator.list_languages()):
            print(f"  • {lang}")
    
    def _generate(self, args: str):
        if not args:
            print("Usage: /generate <language> <prompt>")
            print("Example: /generate python 'function to sort a list'")
            return
        
        parts = args.split(" ", 1)
        if len(parts) < 2:
            print("❌ Please specify both language and prompt")
            return
        
        lang, prompt = parts[0].lower(), parts[1]
        print(f"\n🔧 Generating {lang} code...\n")
        
        result = self.orchestrator.generate(lang, prompt)
        print(result)
    
    def _analyze(self, filepath: str):
        print(f"\n🔍 Analyzing {filepath}...")
        print("(Coming soon)")

if __name__ == "__main__":
    agent = ClawCoder()
    agent.run()
