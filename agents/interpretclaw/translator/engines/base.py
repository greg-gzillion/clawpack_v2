"""Base translation engine interface"""

from abc import ABC, abstractmethod

class TranslationEngine(ABC):
    """Abstract base class for translation engines"""
    
    @abstractmethod
    def translate(self, text: str, target_lang: str, source_lang: str = "auto") -> str:
        """Translate text to target language"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if engine is available"""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Engine name"""
        pass
