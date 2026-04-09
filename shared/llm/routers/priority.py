"""Priority Router - Try providers in order"""
from typing import List
from .base import BaseRouter
from ..providers.base import BaseProvider, LLMResponse

class PriorityRouter(BaseRouter):
    def __init__(self, priority_order: List[str] = None):
        self.priority_order = priority_order or ["openrouter", "anthropic", "ollama"]
    
    def route(self, providers: List[BaseProvider], prompt: str, **kwargs) -> LLMResponse:
        # Create lookup dict
        provider_dict = {p.name: p for p in providers}
        
        # Try in priority order
        for provider_name in self.priority_order:
            if provider_name in provider_dict:
                provider = provider_dict[provider_name]
                if provider.is_available():
                    response = provider.get_response(prompt, **kwargs)
                    if response.text:
                        return response
        
        # Fallback: try any available provider
        for provider in providers:
            if provider.is_available():
                response = provider.get_response(prompt, **kwargs)
                if response.text:
                    return response
        
        return LLMResponse(text="", provider_name="none", response_time=0, model="", error="No providers available")
