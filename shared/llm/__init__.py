"""Main LLM Orchestrator - Puts everything together"""
from typing import List, Optional
from .providers import ProviderRegistry
from .routers import RouterFactory
from .cache import LLMCache
from .providers.base import LLMResponse

class LLMOrchestrator:
    def __init__(self, router_type: str = "priority", enable_cache: bool = True):
        self.providers = ProviderRegistry.create_all()
        self.router = RouterFactory.create(router_type)
        self.cache = LLMCache() if enable_cache else None
    
    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        # Check cache first
        if self.cache:
            cached = self.cache.get(prompt, **kwargs)
            if cached:
                return LLMResponse(
                    text=cached,
                    provider_name="cache",
                    response_time=0,
                    model="cached"
                )
        
        # Route to appropriate provider
        response = self.router.route(self.providers, prompt, **kwargs)
        
        # Cache successful response
        if self.cache and response.text:
            self.cache.set(prompt, response.text, **kwargs)
        
        return response
    
    def get_available_providers(self) -> List[str]:
        return [p.name for p in self.providers if p.is_available()]
    
    def get_stats(self) -> dict:
        return {
            "available_providers": self.get_available_providers(),
            "router_type": self.router.__class__.__name__,
            "cache_enabled": self.cache is not None
        }

# Global instance
_orchestrator = None

def get_llm(router_type: str = "priority") -> LLMOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = LLMOrchestrator(router_type=router_type)
    return _orchestrator
