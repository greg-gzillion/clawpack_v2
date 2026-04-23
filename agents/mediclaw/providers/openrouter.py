"""OpenRouter API Provider"""
import requests
from .base import BaseProvider
from config.settings import Config

class OpenRouterProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "OpenRouter"

    def is_available(self) -> bool:
        return bool(Config.OPENROUTER_KEY)

    def generate(self, prompt: str) -> str:
        if not self.is_available():
            return None
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {Config.OPENROUTER_KEY}", "Content-Type": "application/json"},
                json={"model": "google/gemma-4-26b-a4b-it:free", "messages": [{"role": "user", "content": prompt}], "max_tokens": 2000},
                timeout=60
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
        except:
            pass
        return None
