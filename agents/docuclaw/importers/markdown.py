"""Markdown importer"""
from pathlib import Path
from importers.base import BaseImporter
import re

class MarkdownImporter(BaseImporter):
    name = "markdown"
    extensions = [".md", ".markdown", ".mdown", ".mkd"]
    
    def import_file(self, file_path):
        p = Path(file_path)
        content = p.read_text(encoding='utf-8', errors='ignore')
        return self.extract_text(content)
    
    def extract_text(self, content):
        # Strip markdown syntax
        text = re.sub(r'#{1,6}\s', '', content)
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
        
        return {
            "text": text,
            "format": "markdown",
            "headings": len(re.findall(r'^#{1,6}\s', content, re.MULTILINE)),
            "links": len(re.findall(r'\[.*?\]\(.*?\)', content)),
            "raw": content
        }
