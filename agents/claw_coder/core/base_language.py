"""Base class for all language modules"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class BaseLanguage(ABC):
    """Abstract base class for language-specific code generators"""
    
    name: str = ""
    extensions: List[str] = []
    compilers: List[str] = []
    
    @abstractmethod
    def generate(self, prompt: str, context: str = "") -> str:
        """Generate code from prompt"""
        pass
    
    @abstractmethod
    def analyze(self, code: str) -> Dict:
        """Analyze code and return issues, suggestions"""
        pass
    
    @abstractmethod
    def refactor(self, code: str, suggestion: str) -> str:
        """Refactor code based on suggestion"""
        pass
    
    def get_references(self, topic: str) -> List[str]:
        """Get relevant references for a topic (optional override)"""
        return []
