"""OpenRouter API Provider"""

import requests
from config.settings import Config

class OpenRouterProvider:
    @property
    def name(self):
        return "OpenRouter"
    
    def generate(self, prompt: str) -> str:
        if not Config.OPENROUTER_KEY:
            return None
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {Config.OPENROUTER_KEY}", "Content-Type": "application/json"},
                json={"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}], "max_tokens": 2000},
                timeout=60
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
        except:
            pass
        return None
