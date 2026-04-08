"""Text processor"""
from core.base import BaseProcessor
class TextProcessor(BaseProcessor):
    name = "text"
    extensions = [".txt"]
    def process(self, content, options=None): return content
    def analyze(self, content): return {"words": len(content.split())}
