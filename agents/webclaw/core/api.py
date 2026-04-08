"""WebClaw API - OpenRouter + Ollama fallback"""

import os
import requests
import subprocess
from typing import Optional
from .config import get_config

class WebAPI:
    def __init__(self):
        config = get_config()
        self.api_key = config.get('api_key')

    def ask(self, question: str, context: str = "") -> str:
        """Ask AI with fallback to Ollama"""
        system_prompt = """You are WebClaw, an expert in web technologies, cloud computing, cybersecurity, infrastructure, and online resources. Provide accurate, practical, and actionable answers. Include citations and references when possible."""

        full_prompt = f"{system_prompt}\n\n"
        if context:
            full_prompt += f"Context from references:\n{context}\n\n"
        full_prompt += f"User: {question}\n\nAssistant:"

        # Try OpenRouter first
        if self.api_key:
            try:
                print("🌐 Using OpenRouter API...")
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "deepseek/deepseek-chat",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": question}
                        ],
                        "temperature": 0.3,
                        "max_tokens": 2000
                    },
                    timeout=60
                )
                if response.status_code == 200:
                    return response.json()["choices"][0]["message"]["content"]
                else:
                    print(f"⚠️ API error: {response.status_code}")
            except Exception as e:
                print(f"⚠️ API error: {e}")

        # Fallback to Ollama
        print("🦙 Using Ollama fallback...")
        try:
            result = subprocess.run(
                ["ollama", "run", "deepseek-coder:6.7b", full_prompt],
                capture_output=True,
                text=True,
                timeout=120
            )
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error: {result.stderr}"
        except Exception as e:
            return f"Error: {e}"

    def fetch_url(self, url: str, timeout: int = 30) -> Optional[str]:
        """Fetch URL content with better headers"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            response = requests.get(url, timeout=timeout, headers=headers)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

_api = None

def get_api():
    global _api
    if _api is None:
        _api = WebAPI()
    return _api
