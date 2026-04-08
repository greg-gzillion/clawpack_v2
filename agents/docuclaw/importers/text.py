"""Plain text importer"""
from pathlib import Path
from importers.base import BaseImporter

class TextImporter(BaseImporter):
    name = "text"
    extensions = [".txt", ".text", ".log", ".cfg", ".ini"]
    
    def import_file(self, file_path):
        p = Path(file_path)
        content = p.read_text(encoding='utf-8', errors='ignore')
        return self.extract_text(content)
    
    def extract_text(self, content):
        return {
            "text": content,
            "format": "plain",
            "lines": len(content.split("\n")),
            "words": len(content.split())
        }
