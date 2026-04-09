"""Ollama local provider"""
import aiohttp
import requests
from .provider import LLMProvider

class OllamaProvider(LLMProvider):
    def __init__(self, model: str):
        super().__init__("ollama", model)
    
    def is_available(self) -> bool:
        try:
            resp = requests.get("http://localhost:11434/api/tags", timeout=2)
            return resp.status_code == 200
        except:
            return False
    
    async def call(self, prompt: str, max_tokens: int = 200) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:11434/api/generate",
                json={"model": self.model, "prompt": prompt, 
                      "stream": False, "options": {"num_predict": max_tokens}},
                timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                result = await resp.json()
                return result.get("response", "").strip()
