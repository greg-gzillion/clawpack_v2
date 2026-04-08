"""HTML importer"""
from pathlib import Path
from importers.base import BaseImporter
import re

class HTMLImporter(BaseImporter):
    name = "html"
    extensions = [".html", ".htm", ".xhtml"]
    
    def import_file(self, file_path):
        p = Path(file_path)
        content = p.read_text(encoding='utf-8', errors='ignore')
        return self.extract_text(content)
    
    def extract_text(self, content):
        # Strip HTML tags
        text = re.sub(r'<[^>]+>', ' ', content)
        text = re.sub(r'\s+', ' ', text)
        
        return {
            "text": text.strip(),
            "format": "html",
            "raw": content,
            "title": self._extract_title(content)
        }
    
    def _extract_title(self, content):
        match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        return match.group(1) if match else ""
