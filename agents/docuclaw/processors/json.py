"""JSON processor"""
from core.base import BaseProcessor
import json
class JSONProcessor(BaseProcessor):
    name = "json"
    extensions = [".json"]
    def process(self, content, options=None): return json.dumps(json.loads(content), indent=2)
    def analyze(self, content): return {"keys": len(json.loads(content).keys())}
