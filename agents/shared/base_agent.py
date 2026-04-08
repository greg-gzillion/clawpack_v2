"""Base agent class that all agents inherit from"""

import sys
from pathlib import Path

class BaseAgent:
    """Base agent with WebClaw integration"""
    
    def __init__(self, name: str):
        self.name = name
        self.webclaw_url = "http://localhost:5000"  # WebClaw API endpoint
    
    def ask_webclaw(self, query: str) -> str:
        """Send query to WebClaw for AI response"""
        import requests
        try:
            response = requests.post(
                f"{self.webclaw_url}/llm",
                json={"question": query},
                timeout=60
            )
            if response.status_code == 200:
                return response.json().get("response", "")
        except:
            pass
        return "WebClaw not available"
    
    def fetch_url(self, url: str) -> str:
        """Fetch URL via WebClaw"""
        import requests
        try:
            response = requests.get(
                f"{self.webclaw_url}/fetch",
                params={"url": url},
                timeout=30
            )
            if response.status_code == 200:
                return response.text
        except:
            pass
        return ""
    
    def search_webclaw(self, query: str, category: str = "") -> list:
        """Search references via WebClaw"""
        import requests
        try:
            response = requests.get(
                f"{self.webclaw_url}/search",
                params={"q": query, "category": category},
                timeout=30
            )
            if response.status_code == 200:
                return response.json().get("results", [])
        except:
            pass
        return []
