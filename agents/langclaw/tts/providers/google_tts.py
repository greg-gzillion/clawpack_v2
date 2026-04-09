"""Google TTS Provider - Free text-to-speech using Google Translate"""

import requests
from pathlib import Path
from typing import Optional
from urllib.parse import quote

class GoogleTTSProvider:
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)
    
    def speak(self, text: str, lang: str) -> Optional[Path]:
        """Generate speech using Google Translate TTS"""
        try:
            encoded_text = quote(text)
            url = f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl={lang}&q={encoded_text}"
            
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                cache_file = self.cache_dir / f"google_{lang}_{hash(text)}.mp3"
                cache_file.write_bytes(response.content)
                return cache_file
        except Exception as e:
            print(f"   ⚠️ Google TTS: {e}")
        
        return None
