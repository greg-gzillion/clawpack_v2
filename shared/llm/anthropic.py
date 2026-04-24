"""Anthropic provider"""
import aiohttp
from pathlib import Path
from .provider import LLMProvider

class AnthropicProvider(LLMProvider):
    def __init__(self, model: str = "claude-haiku-4-5-20251001"):
        super().__init__("anthropic", model)
        self.key = self._load_key()
    
    def _load_key(self) -> str:
        env = Path(".env").read_text() if Path(".env").exists() else ""
        for line in env.split('\n'):
            if 'ANTHROPIC_API_KEY=' in line:
                return line.split('=', 1)[1].strip().strip('"').strip("'")
        return ""
    
    async def call(self, prompt: str, max_tokens: int = 2000) -> str:
        headers = {
            "x-api-key": self.key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers, json=data, timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                result = await resp.json()
                return result["content"][0]["text"].strip()
