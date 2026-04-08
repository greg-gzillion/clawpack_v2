"""C++ language module"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.base_language import BaseLanguage
from agents.webclaw_client import WebClawClient

class CppLanguage(BaseLanguage):
    name = "cpp"
    extensions = [".cpp", ".h", ".hpp", ".cc"]
    compilers = ["g++", "clang++", "msvc"]
    
    def __init__(self):
        self.web = WebClawClient()
    
    def generate(self, prompt: str, context: str = "") -> str:
        """Generate C++ code from prompt"""
        full_prompt = f"Generate C++ code for: {prompt}\n\nGenerate modern C++ code:"
        return self._call_ai(full_prompt)
    
    def analyze(self, code: str) -> dict:
        """Analyze C++ code"""
        prompt = f"Analyze this C++ code:\n\n{code}"
        response = self._call_ai(prompt)
        return {"issues": [], "suggestions": [response[:500]]}
    
    def refactor(self, code: str, suggestion: str) -> str:
        """Refactor C++ code"""
        prompt = f"Refactor this C++ code: {suggestion}\n\nCode:\n{code}"
        return self._call_ai(prompt)
    
    def _call_ai(self, prompt: str) -> str:
        try:
            import requests
            response = requests.post("http://localhost:5000/llm", json={"question": prompt}, timeout=60)
            if response.status_code == 200:
                return response.json().get("response", "// Generation failed")
        except:
            pass
        return '// Generated C++ code\n\n#include <iostream>\n\nint main() {\n    std::cout << "Hello, World!" << std::endl;\n    return 0;\n}\n'

