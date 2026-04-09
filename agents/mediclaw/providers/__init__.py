"""Provider Registry - Auto-discovers and prioritizes"""

import sys
from pathlib import Path

# Add parent to path for config
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import Config
from .openrouter import OpenRouterProvider
from .anthropic import AnthropicProvider
from .ollama import OllamaProvider

class ProviderRegistry:
    def __init__(self):
        self.providers = []
        self._init_providers()
    
    def _init_providers(self):
        # Only add providers that have keys
        if Config.OPENROUTER_KEY:
            self.providers.append(OpenRouterProvider())
            print(f"✅ OpenRouter loaded")
        else:
            print("⚠️ OpenRouter: No API key")
        
        if Config.ANTHROPIC_KEY:
            self.providers.append(AnthropicProvider())
            print(f"✅ Anthropic loaded")
        else:
            print("⚠️ Anthropic: No API key")
        
        # Ollama is always added (local)
        self.providers.append(OllamaProvider())
        print(f"✅ Ollama loaded")
    
    def get_available(self):
        return [p.name for p in self.providers if p.is_available()]
    
    def generate(self, prompt: str) -> tuple:
        for provider in self.providers:
            if provider.is_available():
                print(f"   Trying {provider.name}...")
                result = provider.generate(prompt)
                if result:
                    return result, provider.name
        return "No LLM providers available", "None"
