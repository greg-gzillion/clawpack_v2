"""URL Content Fetcher"""

import requests
from bs4 import BeautifulSoup

class URLFetcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch(self, url: str, max_chars: int = 3000) -> dict:
        """Fetch and extract content from a URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove non-content elements
            for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
                element.decompose()
            
            # Find main content
            content = None
            for selector in ['main', 'article', '.content', '#content', '.main-content']:
                content = soup.select_one(selector)
                if content:
                    break
            
            if not content:
                content = soup.body if soup.body else soup
            
            text = content.get_text(separator='\n', strip=True)
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            text = '\n'.join(lines[:80])
            
            return {
                "success": True,
                "url": url,
                "title": soup.title.string if soup.title and soup.title.string else url,
                "content": text[:max_chars] + ("..." if len(text) > max_chars else "")
            }
        except Exception as e:
            return {
                "success": False,
                "url": url,
                "error": str(e)
            }
    
    def fetch_multiple(self, urls: list, max_urls: int = 3) -> list:
        """Fetch multiple URLs"""
        results = []
        for url in urls[:max_urls]:
            results.append(self.fetch(url))
        return results
