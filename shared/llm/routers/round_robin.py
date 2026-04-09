"""Round Robin Router - Distribute across providers"""
from typing import List
from .base import BaseRouter
from ..providers.base import BaseProvider, LLMResponse

class RoundRobinRouter(BaseRouter):
    def __init__(self):
        self._counter = 0
    
    def route(self, providers: List[BaseProvider], prompt: str, **kwargs) -> LLMResponse:
        available = [p for p in providers if p.is_available()]
        if not available:
            return LLMResponse(text="", provider_name="none", response_time=0, model="", error="No providers available")
        
        self._counter = (self._counter + 1) % len(available)
        return available[self._counter].get_response(prompt, **kwargs)
