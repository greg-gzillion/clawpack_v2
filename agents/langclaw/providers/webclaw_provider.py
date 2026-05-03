"""Webclaw Provider - Fetches live translation content from web references"""

import re
import requests
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import quote

class WebclawLangProvider:
    def __init__(self):
        self.refs_path = Path("str(PROJECT_ROOT)/agents/webclaw/references/langclaw")
        self.timeout = 10
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    def get_language_folders(self) -> List[str]:
        if self.refs_path.exists():
            return [d.name for d in self.refs_path.iterdir() if d.is_dir() and len(d.name) == 2]
        return []
    
    def extract_urls_from_references(self, language_code: str) -> Dict[str, List[str]]:
        urls = {"dictionaries": [], "translation_apis": []}
        lang_path = self.refs_path / language_code
        
        if not lang_path.exists():
            return urls
        
        for category in ["dictionaries", "translation_apis"]:
            cat_path = lang_path / category
            if cat_path.exists():
                for md_file in cat_path.glob("*.md"):
                    try:
                        content = md_file.read_text(encoding='utf-8')
                        found_urls = re.findall(r'https?://[^\s\)\]<>"]+', content)
                        for url in found_urls:
                            url = url.rstrip('.,;:!?')
                            if url not in urls[category]:
                                urls[category].append(url)
                    except:
                        pass
        return urls
    
    def fetch_translation_my_memory(self, text: str, target_lang: str) -> Optional[str]:
        try:
            url = f"https://api.mymemory.translated.net/get?q={quote(text)}&langpair=en|{target_lang}"
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                if data.get('responseStatus') == 200:
                    translated = data.get('responseData', {}).get('translatedText', '')
                    if translated and translated.lower() != text.lower():
                        return translated
        except:
            pass
        return None
    
    def fetch_translation_google(self, text: str, target_lang: str) -> Optional[str]:
        try:
            url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl={target_lang}&dt=t&q={quote(text)}"
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0 and len(data[0]) > 0:
                    translated = data[0][0][0]
                    if translated and translated.lower() != text.lower():
                        return translated
        except:
            pass
        return None
