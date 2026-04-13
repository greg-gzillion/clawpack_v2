"""Status Cache"""

import json
from pathlib import Path

class Cache:
    def __init__(self, path: Path = None):
        self.path = path or Path(__file__).parent.parent / "llm_cache.json"
    
    def load(self) -> dict:
        if self.path.exists():
            try:
                return json.loads(self.path.read_text())
            except Exception:
                pass
        return {}
    
    def save(self, providers: list):
        data = {}
        for p in providers:
            if p.status != "untested":
                data[p.config.name] = {
                    "status": p.status,
                    "time": p.response_time
                }
        self.path.write_text(json.dumps(data, indent=2))
    
    def apply(self, providers: list):
        cached = self.load()
        for p in providers:
            if p.config.name in cached:
                p.status = cached[p.config.name].get("status", "untested")
                p.response_time = cached[p.config.name].get("time", 0)
