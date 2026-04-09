"""Anthropic API Provider"""
import requests
import os
from .base import BaseProvider

class AnthropicProvider(BaseProvider):
    def __init__(self, api_key: str = None):
        self._api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self._available = None
    
    @property
    def name(self) -> str:
        return "anthropic"
    
    def is_available(self) -> bool:
        if self._available is None:
            self._available = bool(self._api_key)
        return self._available
    
    def generate(self, prompt: str, system: str = None, model: str = "claude-3-haiku-20240307", **kwargs) -> str:
        if not self.is_available():
            return None
        
        try:
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self._api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "max_tokens": kwargs.get("max_tokens", 2000),
                    "messages": [{"role": "user", "content": prompt}]
                },
                timeout=kwargs.get("timeout", 30)
            )
            if response.status_code == 200:
                return response.json()["content"][0]["text"]
        except Exception as e:
            print(f"Anthropic error: {e}")
        return None
