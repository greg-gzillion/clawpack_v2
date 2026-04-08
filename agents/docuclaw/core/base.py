"""Base processor class"""
from abc import ABC, abstractmethod
class BaseProcessor(ABC):
    name = ""
    extensions = []
    @abstractmethod
    def process(self, content, options=None): pass
    @abstractmethod
    def analyze(self, content): pass
