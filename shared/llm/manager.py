"""LLM Manager with liberated model preference"""
import json
import asyncio
from pathlib import Path
from .ollama import OllamaProvider
from .openrouter import OpenRouterProvider
from .anthropic import AnthropicProvider

class LLMManager:
    def __init__(self, prefer_liberated: bool = True):
        self.providers = []
        self.prefer_liberated = prefer_liberated
        self.load_working_llms()
        self.timeout = 10
    
    def load_working_llms(self):
        config_path = Path("working_llms.json")
        if not config_path.exists():
            return
        
        data = json.loads(config_path.read_text())
        
        # Prioritize liberated models if enabled
        if self.prefer_liberated:
            liberated = [m for m in data if "liberated" in m["model"]]
            standard = [m for m in data if "liberated" not in m["model"]]
            data = liberated + standard
        
        priority_order = ["openrouter", "anthropic", "ollama"]
        
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
        
        # Use liberated models for creative/freeform tasks
        if task in ["creative", "dream", "brainstorm"]:
            for p in self.providers:
                if "liberated" in p.model:
                    return p
        
        return self.providers[0]
    
    def list_providers(self):
        return [str(p) for p in self.providers]
