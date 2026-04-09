"""Real LLM Translation - Robust Import"""

import sys
import asyncio
from pathlib import Path

# Add project root to path - THIS IS THE FIX
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Now try to import - with fallback
try:
    from shared.llm.client import LLMClient
    HAS_LLM = True
except ImportError:
    HAS_LLM = False
    print("⚠️ LLM client not found, using fallback")

class TranslationEngine:
    def __init__(self):
        if HAS_LLM:
            self.client = LLMClient()
        else:
            self.client = None
    
    def translate(self, text: str, target_lang: str) -> dict:
        """Real translation using your LLMs"""
        
        lang_names = {
            "es": "Spanish", "fr": "French", "de": "German", "it": "Italian",
            "pt": "Portuguese", "ja": "Japanese", "ko": "Korean", "zh": "Chinese"
        }
        target_name = lang_names.get(target_lang, target_lang)
        
        # If we have LLM, use it
        if self.client and HAS_LLM:
            prompt = f"Translate this to {target_name}. Return ONLY the translation:\n\n{text}"
            try:
                response = asyncio.run(self.client.call(prompt, max_tokens=100))
                return {
                    "success": True,
                    "original": text,
                    "translated": response.content.strip(),
                    "engine": f"{response.provider.value}"
                }
            except Exception as e:
                # Fall back to simple translation
                pass
        
        # Simple fallback dictionary
        translations = {
            ("hello", "es"): "hola",
            ("good morning", "es"): "buenos días",
            ("thank you", "es"): "gracias",
            ("hello", "fr"): "bonjour",
            ("hello", "de"): "hallo",
        }
        
        key = (text.lower(), target_lang)
        if key in translations:
            return {
                "success": True,
                "original": text,
                "translated": translations[key],
                "engine": "dictionary"
            }
        
        return {
            "success": False,
            "original": text,
            "translated": f"[Connect LLM for full translation]",
            "engine": "none"
        }

class Translator:
    def __init__(self):
        self.engine = TranslationEngine()
    
    def translate(self, text: str, target_lang: str, source_lang: str = None):
        return self.engine.translate(text, target_lang)

class TranslationResult:
    def __init__(self, success, translated_text, original_text, target_lang, engine_used, processing_time=0):
        self.success = success
        self.translated_text = translated_text
        self.original_text = original_text
        self.target_lang = target_lang
        self.engine_used = engine_used
        self.processing_time = processing_time
