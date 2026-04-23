"""Translation Fetcher - Handles API calls and response parsing"""

from typing import Optional, Dict, List
from providers.webclaw_provider import WebclawLangProvider

class TranslationFetcher:
    def __init__(self):
        self.provider = WebclawLangProvider()
    
    def fetch_translation(self, text: str, target_lang: str) -> Optional[Dict]:
        # Try MyMemory first (free)
        translation = self.provider.fetch_translation_my_memory(text, target_lang)
        if translation:
            return {
                "translation": translation,
                "method": "MyMemory API",
                "source": "https://mymemory.translated.net"
            }
        
        # Try Google Translate
        translation = self.provider.fetch_translation_google(text, target_lang)
        if translation:
            return {
                "translation": translation,
                "method": "Google Translate",
                "source": "https://translate.google.com"
            }
        
        return None
    
    def get_dictionary_urls(self, language_code: str) -> List[str]:
        urls = self.provider.extract_urls_from_references(language_code)
        return urls.get("dictionaries", [])
