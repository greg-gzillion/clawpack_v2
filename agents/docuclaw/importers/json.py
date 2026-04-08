"""JSON importer"""
from pathlib import Path
from importers.base import BaseImporter
import json

class JSONImporter(BaseImporter):
    name = "json"
    extensions = [".json", ".geojson"]
    
    def import_file(self, file_path):
        p = Path(file_path)
        content = p.read_text(encoding='utf-8', errors='ignore')
        return self.extract_text(content)
    
    def extract_text(self, content):
        try:
            data = json.loads(content)
            return {
                "text": json.dumps(data, indent=2),
                "format": "json",
                "data": data,
                "keys": list(data.keys()) if isinstance(data, dict) else []
            }
        except:
            return {"text": content, "format": "json", "error": "Invalid JSON"}
