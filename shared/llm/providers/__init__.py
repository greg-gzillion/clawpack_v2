"""Provider Registry - Register and discover providers"""
from typing import Dict, Type, List
from .base import BaseProvider

class ProviderRegistry:
    _providers: Dict[str, Type[BaseProvider]] = {}
    
    @classmethod
    def register(cls, name: str, provider_class: Type[BaseProvider]):
        cls._providers[name] = provider_class
    
    @classmethod
    def get(cls, name: str) -> Type[BaseProvider]:
        return cls._providers.get(name)
    
    @classmethod
    def list_all(cls) -> List[str]:
        return list(cls._providers.keys())
    
    @classmethod
    def create_all(cls) -> List[BaseProvider]:
        return [cls._providers[name]() for name in cls._providers]

# Auto-register providers
from .openrouter import OpenRouterProvider
from .ollama import OllamaProvider
from .anthropic import AnthropicProvider

ProviderRegistry.register("openrouter", OpenRouterProvider)
ProviderRegistry.register("ollama", OllamaProvider)
ProviderRegistry.register("anthropic", AnthropicProvider)
