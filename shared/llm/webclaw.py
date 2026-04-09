"""Webclaw Provider - Web scraping and references"""
import aiohttp
from pathlib import Path
from .provider import LLMProvider

class WebclawProvider(LLMProvider):
    def __init__(self):
        super().__init__("webclaw", "references")
        self.references_path = Path("agents/webclaw/references")
    
    async def search(self, query: str) -> str:
        results = []
        if self.references_path.exists():
            for md_file in self.references_path.rglob("*.md"):
                content = md_file.read_text(encoding='utf-8', errors='ignore')
                if query.lower() in content.lower():
                    results.append(content[:500])
                    if len(results) >= 3:
                        break
        
        if results:
            return "\n---\n".join(results)
        return None
    
    async def call(self, prompt: str, max_tokens: int = 200) -> str:
        return await self.search(prompt) or "No references found"
