"""CrustyClaw Core Engine"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class CrustyEngine:
    def __init__(self):
        self.name = "crustyclaw"
        self.chronicle = self._init_chronicle()
    
    def _init_chronicle(self):
        try:
            from chronicle_bridge import ChronicleBridge
            return ChronicleBridge()
        except:
            return None
    
    def search(self, query: str):
        if self.chronicle:
            return self.chronicle.search(query, "both", 5)
        return []
    
    def stats(self):
        s = {"name": self.name, "chronicle": "disconnected"}
        if self.chronicle:
            s["chronicle"] = self.chronicle.stats()
        return s
