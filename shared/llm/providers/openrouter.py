"""OpenRouter API Provider"""
import requests
import os
from .base import BaseProvider

class OpenRouterProvider(BaseProvider):
    def __init__(self, api_key: str = None):
        self._api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self._available = None
    
    @property
    def name(self) -> str:
        return "openrouter"
    
    def is_available(self) -> bool:
        if self._available is None:
            self._available = bool(self._api_key)
        return self._available
    
    def generate(self, prompt: str, system: str = None, model: str = "google/gemini-2.0-flash-lite-preview-02-05:free", **kwargs) -> str:
        if not self.is_available():
            return None
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"},
                json={"model": model, "messages": messages, "max_tokens": kwargs.get("max_tokens", 2000)},
                timeout=kwargs.get("timeout", 30)
            )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"OpenRouter error: {e}")
        return None
