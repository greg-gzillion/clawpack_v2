"""Smart Router - Route based on task type"""
from typing import List, Dict
from .base import BaseRouter
from ..providers.base import BaseProvider, LLMResponse

class SmartRouter(BaseRouter):
    def __init__(self):
        self.task_mapping: Dict[str, List[str]] = {
            "translation": ["openrouter", "ollama"],
            "code": ["openrouter", "ollama"],
            "legal": ["anthropic", "openrouter", "ollama"],
            "medical": ["openrouter", "anthropic", "ollama"],
            "general": ["openrouter", "ollama", "anthropic"]
        }
    
    def route(self, providers: List[BaseProvider], prompt: str, **kwargs) -> LLMResponse:
        task = kwargs.get("task", "general")
        priority = self.task_mapping.get(task, self.task_mapping["general"])
        
        provider_dict = {p.name: p for p in providers}
        
        for provider_name in priority:
            if provider_name in provider_dict:
                provider = provider_dict[provider_name]
                if provider.is_available():
                    response = provider.get_response(prompt, **kwargs)
                    if response.text:
                        return response
        
        return LLMResponse(text="", provider_name="none", response_time=0, model="", error="No providers available")
