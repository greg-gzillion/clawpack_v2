"""zig language module"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.base_language import BaseLanguage
from agents.webclaw_client import WebClawClient

class ZigLanguage(BaseLanguage):
    name = "zig"
    extensions = ['.zig']
    compilers = ['zig']
    
    def __init__(self):
        self.web = WebClawClient()
    
    def generate(self, prompt: str, context: str = "") -> str:
        full_prompt = f"Generate zig code for: {prompt}"
        return self._call_ai(full_prompt)
    
    def analyze(self, code: str) -> dict:
        return {"issues": [], "suggestions": []}
    
    def refactor(self, code: str, suggestion: str) -> str:
        return code
    
    def _call_ai(self, prompt: str) -> str:
        try:
            import requests
            response = requests.post("http://localhost:5000/llm", json={"question": prompt}, timeout=60)
            if response.status_code == 200:
                return response.json().get("response", f"// zig generation failed")
        except:
            pass
        return f'// Generated zig code\n// ⚡ Language: zig\n'
