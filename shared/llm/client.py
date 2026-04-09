"""Real LLM Integration - Claude, GPT, OpenRouter"""

import os
import json
import asyncio
import aiohttp
from pathlib import Path
from typing import AsyncIterator, Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class LLMProvider(str, Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    OPENROUTER = "openrouter"
    GROQ = "groq"
    OLLAMA = "ollama"

@dataclass
class LLMResponse:
    content: str
    provider: LLMProvider
    model: str
    tokens_used: int
    cost: float
    duration_ms: float
    cached: bool = False

class LLMClient:
    """Production LLM client with auto-fallback"""
    
    def __init__(self):
        self.config = self._load_config()
        self.providers = self._detect_providers()
        self.primary = self.providers[0] if self.providers else None
        print(f"🤖 LLM Client initialized: {len(self.providers)} providers")
    
    def _load_config(self) -> Dict[str, str]:
        """Load API keys from .env"""
        config = {}
        env_path = Path(".env")
        if env_path.exists():
            for line in env_path.read_text().split('\n'):
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip().strip('"').strip("'")
        return config
    
    def _detect_providers(self) -> list:
        """Auto-detect available providers"""
        providers = []
        
        # Check OpenRouter (your working key)
        if self.config.get('OPENROUTER_API_KEY'):
            providers.append({
                'type': LLMProvider.OPENROUTER,
                'key': self.config['OPENROUTER_API_KEY'],
                'model': self.config.get('OPENROUTER_MODEL', 'z-ai/glm-5.1'),
                'base_url': 'https://openrouter.ai/api/v1'
            })
        
        # Check Anthropic
        if self.config.get('ANTHROPIC_API_KEY'):
            providers.append({
                'type': LLMProvider.ANTHROPIC,
                'key': self.config['ANTHROPIC_API_KEY'],
                'model': 'claude-3-5-sonnet-20241022',
                'base_url': 'https://api.anthropic.com/v1'
            })
        
        # Check OpenAI
        if self.config.get('OPENAI_API_KEY'):
            providers.append({
                'type': LLMProvider.OPENAI,
                'key': self.config['OPENAI_API_KEY'],
                'model': 'gpt-4o',
                'base_url': 'https://api.openai.com/v1'
            })
        
        # Check Ollama (local)
        if self._check_ollama():
            providers.append({
                'type': LLMProvider.OLLAMA,
                'model': 'llama3.2:3b',
                'base_url': 'http://localhost:11434'
            })
        
        return providers
    
    def _check_ollama(self) -> bool:
        try:
            import requests
            r = requests.get("http://localhost:11434/api/tags", timeout=2)
            return r.status_code == 200
        except:
            return False
    
    async def call(self, prompt: str, max_tokens: int = 1000, 
                   temperature: float = 0.7) -> LLMResponse:
        """Call LLM with auto-fallback through providers"""
        start = datetime.now()
        
        for provider in self.providers:
            try:
                if provider['type'] == LLMProvider.OPENROUTER:
                    result = await self._call_openrouter(provider, prompt, max_tokens, temperature)
                elif provider['type'] == LLMProvider.ANTHROPIC:
                    result = await self._call_anthropic(provider, prompt, max_tokens, temperature)
                elif provider['type'] == LLMProvider.OPENAI:
                    result = await self._call_openai(provider, prompt, max_tokens, temperature)
                elif provider['type'] == LLMProvider.OLLAMA:
                    result = await self._call_ollama(provider, prompt, max_tokens, temperature)
                else:
                    continue
                
                duration = (datetime.now() - start).total_seconds() * 1000
                return LLMResponse(
                    content=result['content'],
                    provider=provider['type'],
                    model=provider['model'],
                    tokens_used=result.get('tokens', 0),
                    cost=result.get('cost', 0),
                    duration_ms=duration
                )
                
            except Exception as e:
                print(f"⚠️ {provider['type'].value} failed: {str(e)[:50]}")
                continue
        
        raise Exception("All LLM providers failed")
    
    async def _call_openrouter(self, provider: dict, prompt: str, max_tokens: int, temp: float) -> dict:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {provider['key']}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/greg-gzillion/clawpack_v2"
            }
            
            data = {
                "model": provider['model'],
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temp
            }
            
            async with session.post(
                f"{provider['base_url']}/chat/completions",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                result = await resp.json()
                return {
                    "content": result['choices'][0]['message']['content'],
                    "tokens": result.get('usage', {}).get('total_tokens', 0),
                    "cost": 0  # OpenRouter pricing varies
                }
    
    async def _call_anthropic(self, provider: dict, prompt: str, max_tokens: int, temp: float) -> dict:
        async with aiohttp.ClientSession() as session:
            headers = {
                "x-api-key": provider['key'],
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": provider['model'],
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temp
            }
            
            async with session.post(
                f"{provider['base_url']}/messages",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                result = await resp.json()
                return {
                    "content": result['content'][0]['text'],
                    "tokens": result.get('usage', {}).get('input_tokens', 0) + result.get('usage', {}).get('output_tokens', 0),
                    "cost": 0
                }
    
    async def _call_openai(self, provider: dict, prompt: str, max_tokens: int, temp: float) -> dict:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {provider['key']}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": provider['model'],
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temp
            }
            
            async with session.post(
                f"{provider['base_url']}/chat/completions",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                result = await resp.json()
                return {
                    "content": result['choices'][0]['message']['content'],
                    "tokens": result.get('usage', {}).get('total_tokens', 0),
                    "cost": 0
                }
    
    async def _call_ollama(self, provider: dict, prompt: str, max_tokens: int, temp: float) -> dict:
        async with aiohttp.ClientSession() as session:
            data = {
                "model": provider['model'],
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": temp
                }
            }
            
            async with session.post(
                f"{provider['base_url']}/api/generate",
                json=data,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as resp:
                result = await resp.json()
                return {
                    "content": result['response'],
                    "tokens": result.get('eval_count', 0),
                    "cost": 0
                }

# Global instance
_llm_client = None

def get_llm() -> LLMClient:
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
