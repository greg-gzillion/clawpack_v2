"""Python language module"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.base_language import BaseLanguage
from agents.webclaw_client import WebClawClient

class PythonLanguage(BaseLanguage):
    name = "python"
    extensions = [".py", ".pyw", ".pyx"]
    compilers = ["python", "pypy"]
    
    def __init__(self):
        self.web = WebClawClient()
    
    def generate(self, prompt: str, context: str = "") -> str:
        """Generate Python code from prompt"""
        full_prompt = f"""Generate Python code for: {prompt}

Context: {context}

Generate clean, well-documented Python code:
"""
        return self._call_ai(full_prompt)
    
    def analyze(self, code: str) -> dict:
        """Analyze Python code"""
        prompt = f"Analyze this Python code and return issues and suggestions:\n\n{code}"
        response = self._call_ai(prompt)
        return {"issues": [], "suggestions": [response[:500]]}
    
    def refactor(self, code: str, suggestion: str) -> str:
        """Refactor Python code"""
        prompt = f"Refactor this Python code based on suggestion: {suggestion}\n\nCode:\n{code}"
        return self._call_ai(prompt)
    
    def _call_ai(self, prompt: str) -> str:
        """Call AI service via WebClaw"""
        try:
            import requests
            response = requests.post(
                "http://localhost:5000/llm",
                json={"question": prompt},
                timeout=60
            )
            if response.status_code == 200:
                return response.json().get("response", "# Generation failed")
        except Exception as e:
            print(f"Error calling WebClaw: {e}")
        
        return f'# Generated Python code\n\ndef solution():\n    pass\n'

