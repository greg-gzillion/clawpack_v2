"""Core Translator - Main translation logic"""

from typing import Dict, Optional
from fetchers.translation_fetcher import TranslationFetcher

class Translator:
    def __init__(self):
        self.fetcher = TranslationFetcher()
        self.lang_names = {
            "es": "Spanish", "fr": "French", "de": "German", "it": "Italian",
            "pt": "Portuguese", "ja": "Japanese", "ko": "Korean", "zh": "Chinese",
            "ru": "Russian", "ar": "Arabic", "hi": "Hindi", "vi": "Vietnamese",
            "th": "Thai", "tr": "Turkish", "nl": "Dutch", "en": "English"
        }
    
    def get_language_name(self, code: str) -> str:
        return self.lang_names.get(code, code.upper())
    
    def translate(self, text: str, target_lang: str) -> Dict:
        result = {
            "success": False,
            "text": text,
            "target": target_lang,
            "translation": None,
            "method": None,
            "source": None,
            "dictionary_urls": []
        }
        
        # Try to fetch translation
        fetched = self.fetcher.fetch_translation(text, target_lang)
        if fetched:
            result["success"] = True
            result["translation"] = fetched["translation"]
            result["method"] = fetched["method"]
            result["source"] = fetched["source"]
        else:
            # Fall back to dictionary URLs
            result["dictionary_urls"] = self.fetcher.get_dictionary_urls(target_lang)
        
        return result
