"""Base Router Interface"""
from abc import ABC, abstractmethod
from typing import List
from ..providers.base import BaseProvider, LLMResponse

class BaseRouter(ABC):
    @abstractmethod
    def route(self, providers: List[BaseProvider], prompt: str, **kwargs) -> LLMResponse:
        pass
