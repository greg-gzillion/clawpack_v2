"""Base provider interface"""

from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
