"""Core TXclaw Agent - TX Blockchain Specialist"""

import sys
from pathlib import Path

# Add the root directory to path
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from providers.api_provider import api_call
from config.settings import get_webclaw_sources

class TXclawAgent:
    """Main agent for TX blockchain operations"""
    
    def __init__(self):
        self.session = {"queries": [], "sources": get_webclaw_sources()}
    
    def _call(self, prompt: str) -> str:
        """Internal API call wrapper"""
        return api_call(prompt)
    
    def add_query(self, query: str):
        """Track query in session"""
        self.session["queries"].append(query)
    
    def get_stats(self) -> dict:
        """Get session statistics"""
        return {
            "queries": len(self.session["queries"]),
            "sources": len(self.session["sources"])
        }
    
    def webclaw_sources(self) -> list:
        """Get available webclaw sources"""
        return self.session["sources"]
