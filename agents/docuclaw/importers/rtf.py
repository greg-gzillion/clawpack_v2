"""RTF importer"""
from pathlib import Path
from importers.base import BaseImporter
import re

class RTFImporter(BaseImporter):
    name = "rtf"
    extensions = [".rtf"]
    
    def import_file(self, file_path):
        p = Path(file_path)
        content = p.read_text(encoding='utf-8', errors='ignore')
        return self.extract_text(content)
    
    def extract_text(self, content):
        # Very basic RTF text extraction
        text = re.sub(r'\\[a-z]+', ' ', content)
        text = re.sub(r'\{.*?\}', '', text)
        text = re.sub(r'\s+', ' ', text)
        
        return {
            "text": text.strip(),
            "format": "rtf",
            "raw": content[:500]
        }
