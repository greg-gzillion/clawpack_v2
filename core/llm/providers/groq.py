"""Groq Provider"""

import os
from .base import BaseProvider, ProviderConfig

class GroqProvider(BaseProvider):
    def __init__(self, config: ProviderConfig):
        super().__init__(config)
        self.client = None
        self._init_client()
    
    def _init_client(self):
        key = os.getenv("GROQ_API_KEY")
        if key and "gsk_" in key:
            try:
                from groq import Groq
                self.client = Groq(api_key=key)
                self.status = "working"
            except Exception:
                self.status = "failed"
    
    def call(self, prompt: str, timeout: int = 60) -> str:
        if not self.client:
            return None
        try:
            resp = self.client.chat.completions.create(
                model=self.config.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            return resp.choices[0].message.content
        except Exception:
            return None
    
    def test(self) -> bool:
        import time
        start = time.time()
        response = self.call("Say OK", timeout=10)
        self.response_time = time.time() - start
        self.status = "working" if response else "failed"
        return self.status == "working"
