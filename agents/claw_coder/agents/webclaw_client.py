"""Client for communicating with WebClaw agent"""

import requests
import json
from typing import Optional

class WebClawClient:
    """Client to fetch online references from WebClaw"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
    
    def fetch(self, url: str) -> Optional[str]:
        """Fetch URL content via WebClaw"""
        try:
            # Direct fetch for now (will use WebClaw API later)
            response = requests.get(url, timeout=30, headers={
                'User-Agent': 'ClawCoder/1.0'
            })
            if response.status_code == 200:
                return response.text  # Limit size
        except:
            pass
        return None
    
    def search(self, query: str) -> Optional[str]:
        """Search web via WebClaw"""
        # Will implement when WebClaw has search endpoint
        return None
