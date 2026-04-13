"""Base Provider"""

from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class ProviderConfig:
    name: str
    model: str
    capabilities: List[str]
    max_tokens: int = 4096

class BaseProvider(ABC):
    def __init__(self, config: ProviderConfig):
        self.config = config
        self.status = "untested"
        self.response_time = 0.0
    
    @abstractmethod
    def call(self, prompt: str, timeout: int = 60) -> Optional[str]:
        pass
    
    @abstractmethod
    def test(self) -> bool:
        pass
    
    def get_info(self) -> dict:
        return {
            "name": self.config.name,
            "model": self.config.model,
            "status": self.status,
            "response_time": self.response_time,
            "capabilities": self.config.capabilities
        }
