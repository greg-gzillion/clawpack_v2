"""Base LLM Provider Interface"""
from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass

@dataclass
class LLMResponse:
    text: str
    provider_name: str
    response_time: float
    model: str
    error: Optional[str] = None

class BaseProvider(ABC):
    """Abstract base class for all LLM providers"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        pass
    
    @abstractmethod
    def generate(self, prompt: str, system: Optional[str] = None, **kwargs) -> Optional[str]:
        pass
    
    def get_response(self, prompt: str, system: Optional[str] = None, **kwargs) -> LLMResponse:
        import time
        start = time.time()
        result = self.generate(prompt, system, **kwargs)
        return LLMResponse(
            text=result or "",
            provider_name=self.name,
            response_time=time.time() - start,
            model=kwargs.get("model", "default"),
            error=None if result else "No response"
        )
