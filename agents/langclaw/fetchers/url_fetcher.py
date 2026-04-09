"""URL Fetcher - Fetches and extracts content from URLs"""

import requests
from bs4 import BeautifulSoup
from typing import Optional

class URLFetcher:
    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    def fetch_text(self, url: str) -> Optional[str]:
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            return ' '.join(chunk for chunk in chunks if chunk)[:2000]
        except:
            return None
