"""WebClaw AI translation engine"""

import requests
from .base import TranslationEngine

class WebClawEngine(TranslationEngine):
    """Uses WebClaw AI for high-quality translation"""
    
    def __init__(self, url: str = "http://localhost:5000"):
        self.url = url
        self._available = None
    
    @property
    def name(self) -> str:
        return "WebClaw AI"
    
    def is_available(self) -> bool:
        if self._available is None:
            try:
                r = requests.get(f"{self.url}/health", timeout=2)
                self._available = r.status_code == 200
            except:
                self._available = False
        return self._available
    
    def translate(self, text: str, target_lang: str, source_lang: str = "auto") -> str:
        if not self.is_available():
            raise Exception(f"{self.name} not available. Start WebClaw first.")
        
        prompt = f"Translate the following text to {target_lang}. Preserve formatting and meaning:\n\n{text}"
        
        response = requests.post(
            f"{self.url}/llm",
            json={"question": prompt},
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json().get("response", text)
        else:
            raise Exception(f"Translation failed: HTTP {response.status_code}")
