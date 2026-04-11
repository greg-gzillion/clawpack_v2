"""A2A Protocol Client for RustyPyCraw"""

import requests
from typing import Dict, Optional

class A2AClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8765"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health(self) -> Dict:
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.json() if response.ok else {'status': 'error'}
        except:
            return {'status': 'unreachable'}
    
    def chat(self, task: str) -> Dict:
        try:
            response = self.session.post(
                f"{self.base_url}/v1/chat",
                json={'task': task},
                headers={'Content-Type': 'application/json'}
            )
            return response.json() if response.ok else {'status': 'error'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def message(self, agent: str, task: str) -> Dict:
        try:
            response = self.session.post(
                f"{self.base_url}/v1/message/{agent}",
                json={'task': task},
                headers={'Content-Type': 'application/json'}
            )
            return response.json() if response.ok else {'status': 'error'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def discover_agents(self) -> list:
        try:
            response = self.session.get(f"{self.base_url}/v1/agents")
            if response.ok:
                data = response.json()
                return data.get('agents', [])
        except:
            pass
        return []
