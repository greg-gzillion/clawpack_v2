"""TypeScript/JavaScript language module"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.base_language import BaseLanguage
from agents.webclaw_client import WebClawClient

class TypeScriptLanguage(BaseLanguage):
    name = "typescript"
    extensions = [".ts", ".tsx", ".js", ".jsx"]
    compilers = ["tsc", "node"]
    
    def __init__(self):
        self.web = WebClawClient()
    
    def generate(self, prompt: str, context: str = "") -> str:
        """Generate TypeScript code from prompt"""
        full_prompt = f"Generate TypeScript code for: {prompt}"
        return self._call_ai(full_prompt)
    
    def analyze(self, code: str) -> dict:
        prompt = f"Analyze this TypeScript code:\n\n{code}"
        response = self._call_ai(prompt)
        return {"issues": [], "suggestions": [response[:500]]}
    
    def refactor(self, code: str, suggestion: str) -> str:
        prompt = f"Refactor this TypeScript code: {suggestion}\n\nCode:\n{code}"
        return self._call_ai(prompt)
    
    def _call_ai(self, prompt: str) -> str:
        try:
            import requests
            response = requests.post("http://localhost:5000/llm", json={"question": prompt}, timeout=60)
            if response.status_code == 200:
                return response.json().get("response", "// Generation failed")
        except:
            pass
        return '// Generated TypeScript code\n\nfunction hello(): void {\n    console.log("Hello, World!");\n}\n'

