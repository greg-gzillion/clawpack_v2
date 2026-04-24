"""References Handler - WebClaw reference search for TX blockchain"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent.parent))

class ReferenceHandler:
    def __init__(self):
        try:
            from agents.webclaw.providers.webclaw_provider import WebclawProvider
            self.provider = WebclawProvider()
        except:
            self.provider = None

    def search(self, query: str, max_results: int = 5) -> list:
        if self.provider:
            try:
                results = self.provider.search_with_context(f"TX blockchain {query}", max_results)
                return results if results else []
            except:
                pass
        return []

    def format_references(self, refs: list) -> str:
        if not refs:
            return "No references found"
        return "\n".join(f"  - {r}" for r in refs[:5])
