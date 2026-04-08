"""Markdown processor"""
from core.base import BaseProcessor
class MarkdownProcessor(BaseProcessor):
    name = "markdown"
    extensions = [".md"]
    def process(self, content, options=None): return content
    def analyze(self, content): return {"words": len(content.split())}
