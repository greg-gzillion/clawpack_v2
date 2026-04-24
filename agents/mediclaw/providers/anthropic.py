"""Anthropic API Provider"""

import requests
from .base import BaseProvider
from config.settings import Config

class AnthropicProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "Anthropic"
    
    def is_available(self) -> bool:
        return bool(Config.ANTHROPIC_KEY)
    
    def generate(self, prompt: str) -> str:
        if not self.is_available():
            return None
        
        try:
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={"x-api-key": Config.ANTHROPIC_KEY, "anthropic-version": "2023-06-01", "Content-Type": "application/json"},
                json={"model": "claude-haiku-4-5-20251001", "max_tokens": 2000, "messages": [{"role": "user", "content": prompt}]},
                timeout=30
            )
            if response.status_code == 200:
                return response.json()["content"][0]["text"]
        except Exception as e:
            print(f"   Anthropic error: {e}")
        return None
