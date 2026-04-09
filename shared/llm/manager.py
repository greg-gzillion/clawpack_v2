"""LLM Manager with sync support"""
import json
import asyncio
from pathlib import Path
from .ollama import OllamaProvider
from .openrouter import OpenRouterProvider
from .anthropic import AnthropicProvider

class LLMManager:
    def __init__(self):
        self.providers = []
        self.load_working_llms()
        self.timeout = 10
    
    def load_working_llms(self):
        config_path = Path("working_llms.json")
        if not config_path.exists():
            return
        
        data = json.loads(config_path.read_text())
        priority_order = ["openrouter", "ollama", "anthropic"]
        
        for source in priority_order:
            for item in data:
                if item["source"] != source:
                    continue
                model = item["model"]
                try:
                    if source == "ollama":
                        provider = OllamaProvider(model)
                        if provider.is_available():
                            self.providers.append(provider)
                    elif source == "openrouter":
                        provider = OpenRouterProvider(model)
                        if provider.key:
                            self.providers.append(provider)
                    elif source == "anthropic":
                        provider = AnthropicProvider(model)
                        if provider.key:
                            self.providers.append(provider)
                except:
                    pass
    
    def get_best_for_task(self, task: str):
        if not self.providers:
            return None
        
        preferences = {
            "translate": ["openrouter", "ollama"],
            "default": ["openrouter", "ollama"]
        }
        
        for source in preferences.get(task, ["openrouter"]):
            for p in self.providers:
                if p.source == source:
                    return p
        return self.providers[0] if self.providers else None
    
    def call_with_fallback_sync(self, prompt: str, task: str = "default") -> str:
        provider = self.get_best_for_task(task)
        if not provider:
            return "No LLM available"
        
        try:
            return asyncio.run(provider.call(prompt, 150))
        except:
            for fallback in self.providers:
                if fallback != provider:
                    try:
                        return asyncio.run(fallback.call(prompt, 150))
                    except:
                        continue
        return "Request failed"
    
    async def call_with_fallback(self, prompt: str, task: str = "default") -> str:
        return self.call_with_fallback_sync(prompt, task)
    
    def list_providers(self):
        return [str(p) for p in self.providers]
