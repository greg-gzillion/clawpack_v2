"""API Provider - AI Capability"""

import requests
from config.settings import Config

class APIProvider:
    def call(self, prompt: str) -> str:
        if not Config.OPENROUTER_KEY:
            return "❌ API key not configured. Please check .env file."
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {Config.OPENROUTER_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 2000,
                    "temperature": 0.7
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"❌ API Error (HTTP {response.status_code}): {response.text[:200]}"
                
        except requests.exceptions.Timeout:
            return "❌ API timeout - please try again"
        except Exception as e:
            return f"❌ API Exception: {e}"
