"""Base LLM Provider"""
from abc import ABC, abstractmethod
from typing import Optional

class LLMProvider(ABC):
    def __init__(self, source: str, model: str):
        self.source = source
        self.model = model
    
    @abstractmethod
    async def call(self, prompt: str, max_tokens: int = 200) -> Optional[str]:
        pass
    
    def __repr__(self):
        return f"{self.source}:{self.model}"
