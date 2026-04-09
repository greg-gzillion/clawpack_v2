"""Complete LLM Integration with Streaming & Caching"""

import hashlib
import json
from typing import AsyncIterator, Optional, Dict, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field

@dataclass
class CacheEntry:
    response: str
    tokens: int
    created_at: datetime
    expires_at: datetime

class LLMCache:
    """LRU cache for LLM responses"""
    
    def __init__(self, max_size: int = 1000, ttl_minutes: int = 60):
        self.max_size = max_size
        self.ttl = timedelta(minutes=ttl_minutes)
        self._cache: Dict[str, CacheEntry] = {}
        self._access_order: list = []
    
    def _key(self, prompt: str, model: str, **kwargs) -> str:
        data = {"prompt": prompt, "model": model, **kwargs}
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
    
    def get(self, prompt: str, model: str, **kwargs) -> Optional[str]:
        key = self._key(prompt, model, **kwargs)
        if key in self._cache:
            entry = self._cache[key]
            if datetime.now() < entry.expires_at:
                self._access_order.remove(key)
                self._access_order.append(key)
                return entry.response
            else:
                del self._cache[key]
        return None
    
    def set(self, prompt: str, model: str, response: str, tokens: int, **kwargs):
        key = self._key(prompt, model, **kwargs)
        
        if len(self._cache) >= self.max_size:
            oldest = self._access_order.pop(0)
            del self._cache[oldest]
        
        self._cache[key] = CacheEntry(
            response=response,
            tokens=tokens,
            created_at=datetime.now(),
            expires_at=datetime.now() + self.ttl
        )
        self._access_order.append(key)
    
    def clear(self):
        self._cache.clear()
        self._access_order.clear()
    
    def stats(self) -> dict:
        return {
            "size": len(self._cache),
            "max_size": self.max_size,
            "hit_rate": f"{(1 - len(self._cache) / self.max_size) * 100:.1f}%" if self._cache else "0%"
        }

class StreamingLLMClient:
    """Complete LLM client with streaming, caching, and fallback"""
    
    def __init__(self):
        from .client import LLMClient
        self.client = LLMClient()
        self.cache = LLMCache()
        self.streaming_enabled = True
    
    async def stream(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        """Stream response token by token"""
        model = kwargs.get('model', self.client.primary['model'] if self.client.primary else 'default')
        
        # Check cache for non-streaming requests
        if not kwargs.get('stream', True):
            cached = self.cache.get(prompt, model, **kwargs)
            if cached:
                yield cached
                return
        
        full_response = ""
        
        for provider in self.client.providers:
            try:
                if provider['type'].value == 'openrouter':
                    async for chunk in self._stream_openrouter(provider, prompt, **kwargs):
                        full_response += chunk
                        yield chunk
                    break
                elif provider['type'].value == 'anthropic':
                    async for chunk in self._stream_anthropic(provider, prompt, **kwargs):
                        full_response += chunk
                        yield chunk
                    break
            except Exception as e:
                continue
        
        # Cache the full response
        if full_response:
            self.cache.set(prompt, model, full_response, len(full_response) // 4, **kwargs)
    
    async def _stream_openrouter(self, provider: dict, prompt: str, **kwargs) -> AsyncIterator[str]:
        import aiohttp
        
        headers = {
            "Authorization": f"Bearer {provider['key']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": kwargs.get('model', provider['model']),
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": kwargs.get('max_tokens', 1000),
            "temperature": kwargs.get('temperature', 0.7),
            "stream": True
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{provider['base_url']}/chat/completions",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as resp:
                async for line in resp.content:
                    line = line.decode('utf-8').strip()
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data_str)
                            if "choices" in chunk:
                                delta = chunk["choices"][0].get("delta", {})
                                if "content" in delta:
                                    yield delta["content"]
                        except:
                            pass
    
    async def _stream_anthropic(self, provider: dict, prompt: str, **kwargs) -> AsyncIterator[str]:
        import aiohttp
        
        headers = {
            "x-api-key": provider['key'],
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": kwargs.get('model', provider['model']),
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": kwargs.get('max_tokens', 1000),
            "temperature": kwargs.get('temperature', 0.7),
            "stream": True
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{provider['base_url']}/messages",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as resp:
                async for line in resp.content:
                    line = line.decode('utf-8').strip()
                    if line.startswith("data: "):
                        data_str = line[6:]
                        try:
                            chunk = json.loads(data_str)
                            if chunk.get("type") == "content_block_delta":
                                yield chunk.get("delta", {}).get("text", "")
                        except:
                            pass

# Global instance
_streaming_llm = None

def get_streaming_llm() -> StreamingLLMClient:
    global _streaming_llm
    if _streaming_llm is None:
        _streaming_llm = StreamingLLMClient()
    return _streaming_llm
