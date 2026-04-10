#!/usr/bin/env python3
"""Webclaw - Remote Data Fetcher (works with Dataclaw for local data)"""
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Optional
import requests

class Webclaw:
    """Fetches real content from URLs - remote data specialist"""
    
    def __init__(self):
        self.refs_path = Path(__file__).parent / "references"
        self.cache_dir = Path(__file__).parent / "cache"
        self.cache_dir.mkdir(exist_ok=True)
        self.url_index = {}
        self.load_index()
    
    def load_index(self):
        """Load the URL index"""
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
            category = md_file.parent.name
            if category not in self.url_index:
                self.url_index[category] = []
            
            try:
                content = md_file.read_text(encoding='utf-8', errors='ignore')
                urls = re.findall(r'https?://[^\s\)\]\"]+', content)
                
                for url in urls:
                    url = url.rstrip('.,;:!?')
                    self.url_index[category].append(url)  # Store as string, not dict
            except:
                pass
        
        with open(self.cache_dir / "url_index.json", 'w') as f:
            json.dump(self.url_index, f)
        
        total = sum(len(v) for v in self.url_index.values())
        print(f"📚 Indexed {total} URLs across {len(self.url_index)} categories", file=sys.stderr)
    
    def search_urls(self, query: str, category: str = None) -> List[str]:
        """Search for URLs matching query - returns list of URLs"""
        results = []
        query_lower = query.lower()
        categories = [category] if category else self.url_index.keys()
        
        for cat in categories:
            if cat not in self.url_index:
                continue
            for url in self.url_index[cat]:
                if query_lower in url.lower():
                    results.append(url)
                if len(results) >= 10:
                    return results
        return results
    
    def fetch_content(self, url: str) -> Dict:
        """Fetch and extract actual content from URL"""
        try:
            response = requests.get(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10
            )
            html = response.text
            
            # Extract title
            title = url
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.I)
            if title_match:
                title = title_match.group(1).strip()
            
            # Clean text
            text = re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=re.DOTALL | re.I)
            text = re.sub(r'<style[^>]*>.*?</style>', ' ', text, flags=re.DOTALL | re.I)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text)
            content = text[:1500].strip()
            
            return {
                "url": url,
                "title": title,
                "content": content,
                "success": True
            }
        except Exception as e:
            return {"url": url, "error": str(e), "success": False}
    
    def get_material(self, query: str) -> str:
        """Get actual learning material for a query"""
        urls = self.search_urls(query)
        if not urls:
            return f"No resources found for '{query}'"
        
        output = [f"\n📚 LEARNING MATERIAL: {query}\n"]
        
        # Fetch content from first result
        url = urls[0]
        content = self.fetch_content(url)
        
        if content["success"]:
            output.append(f"📖 {content['title']}")
            output.append(f"🔗 {content['url']}")
            output.append(f"\n{content['content']}\n")
        else:
            output.append(f"❌ Could not fetch: {url}")
        
        if len(urls) > 1:
            output.append(f"📚 {len(urls)-1} more resources available")
        
        return '\n'.join(output)
    
    def process_command(self, cmd: str) -> str:
        """Process a command"""
        cmd = cmd.strip()
        
        if cmd.startswith("search "):
            query = cmd[7:].strip()
            urls = self.search_urls(query)
            if urls:
                output = [f"Found {len(urls)} resources for '{query}':"]
                for url in urls[:5]:
                    output.append(f"  • {url}")
                return '\n'.join(output)
            return f"No resources found for '{query}'"
        
        elif cmd.startswith("material "):
            query = cmd[9:].strip()
            return self.get_material(query)
        
        elif cmd.startswith("fetch "):
            url = cmd[6:].strip()
            result = self.fetch_content(url)
            if result["success"]:
                return f"📖 {result['title']}\n\n{result['content']}"
            return f"Error: {result.get('error', 'Failed to fetch')}"
        
        elif cmd == "/stats":
            total = sum(len(v) for v in self.url_index.values())
            return f"Categories: {len(self.url_index)} | URLs: {total}"
        
        elif cmd == "/help":
            return """
🌐 WEBCLAW (Remote Data):
  search <query>    - Find resource URLs
  material <query>  - Get actual content from URL
  fetch <url>       - Fetch specific URL

📊 DATACLAW (Local Data):
  Use dataclaw for local files, CSV, JSON, databases
  WebClaw + Dataclaw = Complete data coverage
"""
        elif cmd:
            return self.process_command(f"search {cmd}")
        return ""

def main():
    webclaw = Webclaw()
    
    if len(sys.argv) > 1:
        cmd = ' '.join(sys.argv[1:])
        result = webclaw.process_command(cmd)
        if result:
            print(result)
        return
    
    print("\n🌐 WEBCLAW - Remote Data Fetcher")
    print("Commands: search, material, fetch, /stats, /help, /quit")
    
    while True:
        try:
            cmd = input("\n🌐 > ").strip()
            if cmd == "/quit":
                break
            if cmd:
                result = webclaw.process_command(cmd)
                if result:
                    print(result)
        except (KeyboardInterrupt, EOFError):
            break

if __name__ == "__main__":
    main()
