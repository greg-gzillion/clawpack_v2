"""OpenRouter provider"""
import aiohttp
from pathlib import Path
from .provider import LLMProvider

class OpenRouterProvider(LLMProvider):
    def __init__(self, model: str):
        super().__init__("openrouter", model)
        self.key = self._load_key()
    
    def _load_key(self) -> str:
        env = Path(".env").read_text() if Path(".env").exists() else ""
        for line in env.split('\n'):
            if 'OPENROUTER_API_KEY=' in line:
                return line.split('=', 1)[1].strip().strip('"').strip("'")
        return ""
    
    async def call(self, prompt: str, max_tokens: int = 200) -> str:
        headers = {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers, json=data, timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                result = await resp.json()
                return result["choices"][0]["message"]["content"].strip()
