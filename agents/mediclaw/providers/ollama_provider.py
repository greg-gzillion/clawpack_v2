"""Ollama local provider"""

import requests
from .base import BaseProvider
from config.settings import Config

class OllamaProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "Ollama"
    
    def generate(self, prompt: str) -> str:
        for model in Config.OLLAMA_MODELS:
            try:
                response = requests.post(
                    f"{Config.OLLAMA_URL}/api/generate",
                    json={"model": model, "prompt": prompt, "stream": False},
                    timeout=90
                )
                if response.status_code == 200:
                    result = response.json().get("response", "")
                    if result and len(result) > 10:
                        return f"[{model}]\n{result}"
            except:
                continue
        return None
