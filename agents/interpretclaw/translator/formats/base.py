"""Base document format handler"""

from abc import ABC, abstractmethod
from pathlib import Path

class DocumentFormat(ABC):
    """Abstract base class for document format handlers"""
    
    @abstractmethod
    def extract(self, file_path: Path) -> str:
        """Extract text from document"""
        pass
    
    @abstractmethod
    def save(self, file_path: Path, content: str, target_lang: str) -> Path:
        """Save translated document"""
        pass
    
    @property
    @abstractmethod
    def supported_extensions(self) -> list:
        """List of supported file extensions"""
        pass
