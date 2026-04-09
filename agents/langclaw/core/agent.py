"""Langclaw Agent - Standalone"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from audio.tts_engine import TTSEngine
from core.session_manager import SessionManager

class LangclawAgent:
    def __init__(self):
        self.tts = TTSEngine()
        self.session = SessionManager()
        self.lang_names = {
            "es": "Spanish", "fr": "French", "de": "German", "it": "Italian",
            "pt": "Portuguese", "ja": "Japanese", "ko": "Korean", "zh": "Chinese"
        }
    
    def get_available_languages(self):
        return list(self.lang_names.keys())
    
    def get_language_name(self, code: str) -> str:
        return self.lang_names.get(code, code)
    
    def translate(self, text: str, target: str) -> str:
        # Simple mock translation for now
        translations = {
            ("hello", "es"): "hola",
            ("goodbye", "es"): "adiós",
            ("thank you", "es"): "gracias",
            ("hello", "fr"): "bonjour",
            ("goodbye", "fr"): "au revoir"
        }
        key = (text.lower(), target)
        return translations.get(key, f"[{text} in {self.get_language_name(target)}]")
    
    def speak(self, text: str, lang: str = "en"):
        return self.tts.speak(text, lang)
    
    def get_stats(self):
        return self.session.get_stats()
