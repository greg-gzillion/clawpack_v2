"""OpenRouter API provider"""

import requests
from .base import BaseProvider
from config.settings import Config

class OpenRouterProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "OpenRouter"
    
    def generate(self, prompt: str) -> str:
        if not Config.OPENROUTER_KEY:
            return None
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {Config.OPENROUTER_KEY}", "Content-Type": "application/json"},
                json={"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}], "max_tokens": 2000},
                timeout=60
            )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
        except:
            pass
        return None
