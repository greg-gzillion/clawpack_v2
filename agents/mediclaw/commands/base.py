"""Base Command"""

from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def name(self) -> str:
        pass
    
    @abstractmethod
    def execute(self, args: str, engine) -> str:
        pass
