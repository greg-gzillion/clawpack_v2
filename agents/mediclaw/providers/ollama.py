"""Ollama Local Provider"""

import requests
from .base import BaseProvider
from config.settings import Config

class OllamaProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "Ollama"
    
    def is_available(self) -> bool:
        try:
            r = requests.get(f"{Config.OLLAMA_URL}/api/tags", timeout=2)
            return r.status_code == 200
        except:
            return False
    
    def generate(self, prompt: str) -> str:
        if not self.is_available():
            return None
        
        try:
            response = requests.post(
                f"{Config.OLLAMA_URL}/api/generate",
                json={"model": Config.OLLAMA_MODEL, "prompt": prompt, "stream": False},
                timeout=120
            )
            if response.status_code == 200:
                return response.json().get("response")
        except Exception as e:
            print(f"   Ollama error: {e}")
        return None
