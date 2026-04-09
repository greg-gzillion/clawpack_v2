"""URL Fetcher for TXclaw - Retrieves content from TX.org URLs"""

import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict
import time

class URLFetcher:
    """Fetch and parse content from URLs"""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        self.cache: Dict[str, tuple] = {}
    
    def fetch(self, url: str) -> Optional[str]:
        """Fetch and extract text content from URL"""
        if url in self.cache:
            content, timestamp = self.cache[url]
            if time.time() - timestamp < 300:  # 5 minute cache
                return content
        
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Limit to first 2000 characters
            result = text[:2000] + "..." if len(text) > 2000 else text
            
            self.cache[url] = (result, time.time())
            return result
            
        except requests.RequestException as e:
            return None
    
    def fetch_tx_explorer(self, tx_hash: str) -> Optional[str]:
        """Fetch transaction from TX.org explorer"""
        url = f"https://explorer.tx.org/tx/{tx_hash}"
        return self.fetch(url)
    
    def fetch_tx_block(self, block_height: str) -> Optional[str]:
        """Fetch block from TX.org explorer"""
        url = f"https://explorer.tx.org/block/{block_height}"
        return self.fetch(url)
    
    def fetch_tx_address(self, address: str) -> Optional[str]:
        """Fetch address from TX.org explorer"""
        url = f"https://explorer.tx.org/address/{address}"
        return self.fetch(url)
