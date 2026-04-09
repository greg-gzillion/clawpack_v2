"""Ollama Local Provider"""
import requests
from .base import BaseProvider

class OllamaProvider(BaseProvider):
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self._available = None
    
    @property
    def name(self) -> str:
        return "ollama"
    
    def is_available(self) -> bool:
        if self._available is None:
            try:
                r = requests.get(f"{self.base_url}/api/tags", timeout=2)
                self._available = r.status_code == 200
            except:
                self._available = False
        return self._available
    
    def generate(self, prompt: str, system: str = None, model: str = "llama3.2:3b", **kwargs) -> str:
        if not self.is_available():
            return None
        
        payload = {"model": model, "prompt": prompt, "stream": False}
        if system:
            payload["system"] = system
        
        try:
            response = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=kwargs.get("timeout", 60))
            if response.status_code == 200:
                return response.json().get("response", "")
        except Exception as e:
            print(f"Ollama error: {e}")
        return None
