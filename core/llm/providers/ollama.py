"""Ollama Provider"""

import subprocess
from .base import BaseProvider, ProviderConfig

class OllamaProvider(BaseProvider):
    def call(self, prompt: str, timeout: int = 60) -> str:
        try:
            result = subprocess.run(
                ["ollama", "run", self.config.model, prompt],
                capture_output=True, text=False, timeout=timeout, shell=False
            )
            if result.returncode == 0:
                return result.stdout.decode("utf-8", errors="replace").strip()
        except Exception:
            pass
        return None
    
    def test(self) -> bool:
        import time
        start = time.time()
        response = self.call("Say OK", timeout=120)
        self.response_time = time.time() - start
        self.status = "working" if response else "failed"
        return self.status == "working"
