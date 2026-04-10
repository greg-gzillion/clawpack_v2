#!/usr/bin/env python3
"""Webclaw - Remote Data Fetcher with safe HTML parsing"""
import sys
import json
import re
import hashlib
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import requests
from html.parser import HTMLParser

class SafeHTMLParser(HTMLParser):
    """Safe HTML parser that extracts text without regex vulnerabilities"""
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.skip_tags = {'script', 'style', 'nav', 'footer', 'header'}
        self.current_tag = None
    
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
    
    def handle_endtag(self, tag):
        self.current_tag = None
    
    def handle_data(self, data):
        if self.current_tag not in self.skip_tags:
            text = data.strip()
            if text:
                self.text_parts.append(text)
    
    def get_text(self):
        return ' '.join(self.text_parts)

class Webclaw:
    """Fetches real content from URLs with safe parsing"""
    
    def __init__(self):
        self.refs_path = Path(__file__).parent / "references"
        self.cache_dir = Path(__file__).parent / "cache"
        self.memory_dir = Path(__file__).parent.parent.parent / "data" / "shared_memory"
        self.cache_dir.mkdir(exist_ok=True)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        self.cache_ttl_hours = 168
        self.url_index = {}
        self.content_cache = {}
        
        self.load_index()
        self.load_shared_memory()
    
    def load_index(self):
        """Load the URL index from cache"""
        cache_file = self.cache_dir / "url_index.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    self.url_index = json.load(f)
                total = sum(len(v) for v in self.url_index.values())
                print(f"📚 Loaded {total} URLs from cache", file=sys.stderr)
                return
            except:
                pass
        self.build_url_index()
    
    def build_url_index(self):
        """Index all URLs from reference files"""
        print("📚 Building URL index...", file=sys.stderr)
        for md_file in self.refs_path.rglob("*.md"):
            category = str(md_file.relative_to(self.refs_path).parent)
            if category not in self.url_index:
                self.url_index[category] = []
            
            try:
                content = md_file.read_text(encoding='utf-8', errors='ignore')
                # Safe URL extraction with simple regex (no catastrophic backtracking)
                urls = re.findall(r'https?://[^\s<>"\'()\[\]{}]+', content)
                
                for url in urls:
                    url = url.rstrip('.,;:!?')
                    self.url_index[category].append({
                        "url": url,
                        "source": str(md_file),
                        "category": category
                    })
            except:
                pass
        
        with open(self.cache_dir / "url_index.json", 'w') as f:
            json.dump(self.url_index, f, indent=2)
        
        total = sum(len(v) for v in self.url_index.values())
        print(f"📚 Indexed {total} URLs across {len(self.url_index)} categories", file=sys.stderr)
    
    def load_shared_memory(self):
        """Load shared memory from data directory"""
        memory_file = self.memory_dir / "webclaw_memory.json"
        if memory_file.exists():
            try:
                with open(memory_file, 'r') as f:
                    self.shared_memory = json.load(f)
            except:
                self.shared_memory = {}
        else:
            self.shared_memory = {}
    
    def get_cache_key(self, url: str) -> str:
        """Generate cache key from URL"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def fetch_content_safe(self, url: str) -> Dict:
        """Fetch and extract content using safe HTML parsing"""
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Use safe HTML parser instead of regex
            parser = SafeHTMLParser()
            parser.feed(response.text)
            text = parser.get_text()
            
            # Extract title safely
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', response.text, re.I)
            title = title_match.group(1).strip() if title_match else url
            
            # Clean up whitespace
            text = re.sub(r'\s+', ' ', text)
            content = text[:3000].strip()
            
            return {
                "url": url,
                "title": title,
                "content": content,
                "success": True
            }
        except Exception as e:
            return {"url": url, "error": str(e), "success": False}
    
    def search_urls(self, query: str, category: str = None) -> List[str]:
        """Search for URLs matching query"""
        results = []
        query_lower = query.lower()
        categories = [category] if category else self.url_index.keys()
        
        for cat in categories:
            if cat not in self.url_index:
                continue
            for item in self.url_index[cat]:
                url = item.get("url", item) if isinstance(item, dict) else item
                if query_lower in url.lower():
                    results.append(url)
                if len(results) >= 10:
                    return results
        return results
    
    def get_material(self, query: str) -> str:
        """Get actual readable material for a query"""
        urls = self.search_urls(query)
        if not urls:
            return f"No resources found for '{query}'"
        
        output = []
        for url in urls[:3]:
            content = self.fetch_content_safe(url)
            if content["success"]:
                output.append(f"\n📖 {content['title']}\n🔗 {content['url']}\n{content['content'][:500]}")
            else:
                output.append(f"\n❌ Could not fetch: {url}")
        
        return '\n'.join(output) if output else f"No content for '{query}'"
    
    def process_command(self, cmd: str) -> str:
        """Process a command"""
        cmd = cmd.strip()
        
        if cmd.startswith("search "):
            query = cmd[7:].strip()
            urls = self.search_urls(query)
            if urls:
                return f"Found {len(urls)} resources:\n" + '\n'.join(f"  • {u}" for u in urls[:10])
            return f"No resources found for '{query}'"
        
        elif cmd.startswith("material "):
            query = cmd[9:].strip()
            return self.get_material(query)
        
        elif cmd.startswith("fetch "):
            url = cmd[6:].strip()
            content = self.fetch_content_safe(url)
            if content["success"]:
                return f"📖 {content['title']}\n\n{content['content']}"
            return f"Error: {content.get('error', 'Failed')}"
        
        return ""

def main():
    webclaw = Webclaw()
    if len(sys.argv) > 1:
        print(webclaw.process_command(' '.join(sys.argv[1:])))
    else:
        print("Webclaw - Web content fetcher")
        print("Commands: search, material, fetch")

if __name__ == "__main__":
    main()
