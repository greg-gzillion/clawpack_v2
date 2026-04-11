#!/usr/bin/env python3
"""liberateclaw - Model Liberation Agent"""

import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

class liberateclawAgent:
    def __init__(self):
        self.name = "liberateclaw"
        self.description = "Model Liberation - Download and manage local LLM models"
        self.liberated_dir = Path.home() / ".clawpack" / "liberated"
        self.liberated_dir.mkdir(parents=True, exist_ok=True)
    
    def handle(self, cmd: str) -> str:
        cmd = cmd.strip()
        
        if cmd == "/help" or cmd == "help":
            return self._help()
        elif cmd == "/models" or cmd == "models":
            return self._list_ollama_models()
        elif cmd == "/liberated":
            return self._list_liberated()
        elif cmd.startswith("/liberate "):
            return self._liberate(cmd[10:].strip())
        elif cmd.startswith("/use "):
            parts = cmd[5:].split(maxsplit=1)
            if len(parts) == 2:
                return self._use_model(parts[0], parts[1])
            return "Usage: /use <model> <prompt>"
        else:
            return f"Unknown: {cmd}\n{self._help()}"
    
    def process(self, command, *args):
        return self.handle(' '.join(args))
    

    def collaborate(self, target_agent: str, task: str) -> str:
        """Collaborate with another agent via A2A"""
        try:
            import requests
            response = requests.post(
                f"http://127.0.0.1:8766/v1/message/{target_agent}",
                json={"task": task},
                timeout=60
            )
            if response.status_code == 200:
                result = response.json()
                return f"🤝 {target_agent.upper()} responded:
{result.get('result', 'No result')[:500]}"
            return f"❌ Agent {target_agent} not responding"
        except Exception as e:
            return f"❌ Collaboration error: {e}"

    def _help(self):
        return """
LiberateClaw - Model Liberation Agent

Commands:
  /models              - List available Ollama models
  /liberate <model>    - Download/liberate a model
  /liberated           - List liberated models
  /use <model> <prompt> - Use a liberated model
  /help                - Show this help

Examples:
  /liberate tinyllama:1.1b
  /use tinyllama:1.1b "Explain AI"
"""
    
    def _list_ollama_models(self):
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            if result.returncode == 0:
                return f"📦 Available Models:\n{result.stdout}"
            return "Error listing models"
        except Exception as e:
            return f"Error: {e}"
    
    def _list_liberated(self):
        models = list(self.liberated_dir.glob("*"))
        if not models:
            return "No liberated models yet. Use /liberate <model>"
        output = f"🔓 Liberated Models ({len(models)}):\n"
        for m in models:
            output += f"  • {m.name}\n"
        return output
    
    def _liberate(self, model):
        model_slug = model.replace(':', '_').replace('/', '_')
        model_dir = self.liberated_dir / model_slug
        if model_dir.exists():
            return f"Model {model} already liberated"
        
        try:
            result = subprocess.run(['ollama', 'pull', model], capture_output=True, text=True)
            if result.returncode == 0:
                model_dir.mkdir(parents=True, exist_ok=True)
                (model_dir / "info.json").write_text(json.dumps({
                    "model": model, "liberated_at": datetime.now().isoformat()
                }, indent=2))
                return f"✅ Liberated: {model}"
            return f"❌ Failed: {result.stderr}"
        except Exception as e:
            return f"Error: {e}"
    
    def _use_model(self, model, prompt):
        model_slug = model.replace(':', '_').replace('/', '_')
        model_dir = self.liberated_dir / model_slug
        if not model_dir.exists():
            return f"Model {model} not liberated. Use /liberate {model} first"
        
        try:
            result = subprocess.run(['ollama', 'run', model, prompt], capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                return f"🤖 {model}:\n{result.stdout[:1000]}"
            return f"Error: {result.stderr}"
        except subprocess.TimeoutExpired:
            return "Model inference timed out"
        except Exception as e:
            return f"Error: {e}"

def main():
    agent = liberateclawAgent()
    if len(sys.argv) > 1:
        print(agent.handle(' '.join(sys.argv[1:])))
    else:
        print(agent._help())

if __name__ == "__main__":
    main()
