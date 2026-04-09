"""Langclaw - Language translation agent with all patterns integrated"""

import sys
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.agent import BaseAgent
from shared.loop import ToolSafety
from shared.memory import MemoryType


class LangclawAgent(BaseAgent):
    """Language translation and speech agent"""
    
    def __init__(self, project_root: Optional[Path] = None):
        super().__init__("Langclaw", project_root)
        
        # Load language references
        references_path = Path("C:/Users/greg/dev/clawpack_v2/agents/webclaw/references/langclaw")
        self.load_references(references_path)
        
        # Langclaw-specific state
        self.supported_languages = [
            "es", "fr", "de", "it", "pt", "ja", "ko", "zh", 
            "ru", "ar", "hi", "vi", "th", "tr", "nl", "en"
        ]
    
    def _register_tools(self):
        """Register Langclaw-specific tools"""
        self.register_tool("translate", self.translate, ToolSafety.READ_ONLY)
        self.register_tool("speak", self.speak, ToolSafety.READ_ONLY)
        self.register_tool("listen", self.listen, ToolSafety.READ_ONLY)
        self.register_tool("detect_language", self.detect_language, ToolSafety.READ_ONLY)
    
    def translate(self, text: str, target_lang: str, source_lang: str = "en") -> Dict:
        """
        Translate text to target language.
        
        Args:
            text: Text to translate
            target_lang: Target language code (es, fr, de, etc.)
            source_lang: Source language code (default: en)
        
        Returns:
            Dictionary with translation and metadata
        """
        # Search references first
        refs = self.search_references(f"{text} {target_lang}")
        
        # Try memory recall for similar translations
        memory_context = self.recall(f"translate {text} to {target_lang}")
        
        # This would call translation API
        # Placeholder implementation
        translations = {
            ("hello", "es"): "hola",
            ("goodbye", "es"): "adiós",
            ("thank you", "es"): "gracias",
            ("hello", "fr"): "bonjour",
            ("goodbye", "fr"): "au revoir",
            ("thank you", "fr"): "merci"
        }
        
        key = (text.lower(), target_lang)
        translation = translations.get(key, text)
        
        result = {
            "text": text,
            "translation": translation,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "references": len(refs),
            "from_memory": bool(memory_context)
        }
        
        # Record successful translation
        self.remember(
            MemoryType.FEEDBACK,
            f"Translation: {text} -> {translation}",
            f"Translated '{text}' to {target_lang}",
            f"Source: {source_lang}, Target: {target_lang}, Result: {translation}"
        )
        
        return result
    
    def speak(self, text: str, lang: str = "en") -> Dict:
        """
        Text-to-speech for given text.
        
        Args:
            text: Text to speak
            lang: Language code for pronunciation
        
        Returns:
            Dictionary with TTS result
        """
        # This would call TTS engine
        return {
            "text": text,
            "lang": lang,
            "spoken": True,
            "method": "google_tts"
        }
    
    def listen(self, duration: int = 5) -> Dict:
        """
        Speech-to-text from microphone.
        
        Args:
            duration: Recording duration in seconds
        
        Returns:
            Dictionary with transcribed text
        """
        # This would call STT engine
        return {
            "transcribed": "Hello world",
            "duration": duration,
            "confidence": 0.95
        }
    
    def detect_language(self, text: str) -> Dict:
        """
        Detect language of given text.
        
        Args:
            text: Text to analyze
        
        Returns:
            Dictionary with detected language and confidence
        """
        # Simple heuristic-based detection
        lang_markers = {
            "es": ["hola", "gracias", "adiós"],
            "fr": ["bonjour", "merci", "au revoir"],
            "de": ["hallo", "danke", "auf wiedersehen"]
        }
        
        text_lower = text.lower()
        detected = "en"
        confidence = 0.5
        
        for lang, markers in lang_markers.items():
            if any(m in text_lower for m in markers):
                detected = lang
                confidence = 0.8
                break
        
        return {
            "text": text,
            "detected_lang": detected,
            "confidence": confidence
        }
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported language codes"""
        return self.supported_languages


# Register the agent
from shared.agent import ClawpackAgentRegistry
ClawpackAgentRegistry.register("langclaw", LangclawAgent)
