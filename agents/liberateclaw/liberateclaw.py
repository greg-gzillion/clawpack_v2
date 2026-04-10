#!/usr/bin/env python3
"""liberateclaw - Model Liberation Agent"""
import sys
import subprocess
import json
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.base_agent import BaseAgent

class liberateclawCore:
    """Core processing logic for model liberation"""
    
    def __init__(self):
        self.liberated_dir = Path.home() / ".clawpack" / "liberated"
        self.liberated_dir.mkdir(parents=True, exist_ok=True)
    
    def process(self, query: str) -> str:
        cmd = query.strip().lower()
        
        if cmd == "/help":
            return self._help()
        elif cmd == "/stats":
            return self._stats()
        elif cmd == "/liberated":
            return self._list_liberated()
        elif cmd.startswith("/liberate "):
            return self._liberate(cmd[10:].strip())
        elif cmd.startswith("/use "):
            return self._use_liberated(cmd[5:].strip())
        else:
            return f"Unknown: {cmd}. Type /help"
    
    def _help(self) -> str:
        return """
🦞 LIBERATECLAW - Model Liberation Agent

Commands:
  /help                 - Show this help
  /stats                - Show statistics
  /liberated            - List liberated models
  /liberate <model>     - Liberate a model
  /use <model> <prompt> - Use a liberated model

Examples:
  /liberate llama3.2:3b
  /use llama3.2:3b "Tell me a story"
"""
    
    def _stats(self) -> str:
        count = len(list(self.liberated_dir.glob("*")))
        return f"Liberated models: {count}\nDirectory: {self.liberated_dir}"
    
    def _list_liberated(self) -> str:
        models = list(self.liberated_dir.glob("*"))
        if not models:
            return "No liberated models yet. Use /liberate <model>"
        return "Liberated models:\n" + "\n".join(f"  • {m.name}" for m in models)
    
    def _liberate(self, model: str) -> str:
        model_slug = model.replace("/", "_").replace(":", "_")
        model_dir = self.liberated_dir / model_slug
        model_dir.mkdir(exist_ok=True)
        
        info = {"model": model, "liberated": True}
        (model_dir / "info.json").write_text(json.dumps(info, indent=2))
        
        return f"✅ Liberated {model}\nSaved to {model_dir}"
    
    def _use_liberated(self, args: str) -> str:
        parts = args.split(maxsplit=1)
        if len(parts) < 2:
            return "Usage: /use <model> <prompt>"
        
        model, prompt = parts
        model_slug = model.replace("/", "_").replace(":", "_")
        model_dir = self.liberated_dir / model_slug
        
        if not model_dir.exists():
            return f"❌ Model '{model}' not liberated. Use /liberate first."
        
        try:
            result = subprocess.run(
                ["ollama", "run", model, prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.stdout.strip() if result.stdout else f"Error: {result.stderr}"
        except Exception as e:
            return f"Error: {e}"

class liberateclawAgent(BaseAgent):
    def __init__(self):
        super().__init__("liberateclaw")
        self.core = liberateclawCore()
    
    def handle(self, query: str) -> str:
        self.track_interaction()
        return self.core.process(query)

def main():
    agent = liberateclawAgent()
    
    if len(sys.argv) > 1:
        cmd = ' '.join(sys.argv[1:])
        print(agent.handle(cmd))
        return
    
    print("\n🎯 liberateclaw - Model Liberation Agent")
    print("Type /help for commands, /quit to exit")
    
    while True:
        try:
            cmd = input("\nliberate> ").strip()
            if cmd == "/quit":
                break
            if cmd:
                result = agent.handle(cmd)
                if result:
                    print(result)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
