#!/usr/bin/env python3
"""Webclaw - Fetches content from URLs with citations"""
import sys
import json
import re
import requests
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup

class Webclaw:
    def __init__(self):
        self.cache_dir = Path(__file__).parent / "cache"
        self.cache_dir.mkdir(exist_ok=True)
    
    def fetch_with_citation(self, url: str) -> dict:
        """Fetch URL content and return with citation"""
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script/style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Get title
            title = soup.title.string if soup.title else urlparse(url).netloc
            
            # Get main content
            content_selectors = ['main', 'article', '.content', '#content', 'body']
            content_elem = None
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    break
            
            text = content_elem.get_text() if content_elem else soup.get_text()
            
            # Clean text
            lines = (line.strip() for line in text.splitlines())
            text = '\n'.join(line for line in lines if line)
            
            return {
                "success": True,
                "url": url,
                "title": title.strip(),
                "content": text[:2000],  # First 2000 chars
                "citation": f"Source: {urlparse(url).netloc}\nTitle: {title}\nRetrieved: {response.headers.get('date', 'Unknown')}"
            }
        except Exception as e:
            return {"success": False, "url": url, "error": str(e)}
    
    def process_command(self, cmd: str) -> str:
        if cmd.startswith("fetch "):
            url = cmd[6:].strip()
            result = self.fetch_with_citation(url)
            if result["success"]:
                return f"""
📖 {result['title']}
🔗 {result['url']}
📅 {result['citation']}

{result['content']}
"""
            return f"❌ Error: {result.get('error', 'Unknown')}"
        return ""

def main():
    w = Webclaw()
    if len(sys.argv) > 1:
        print(w.process_command(' '.join(sys.argv[1:])))
    else:
        print("Webclaw - Content fetcher")

if __name__ == "__main__":
    main()
