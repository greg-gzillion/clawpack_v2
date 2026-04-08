"""XML importer"""
from pathlib import Path
from importers.base import BaseImporter
import xml.etree.ElementTree as ET

class XMLImporter(BaseImporter):
    name = "xml"
    extensions = [".xml", ".xsd", ".xsl"]
    
    def import_file(self, file_path):
        p = Path(file_path)
        content = p.read_text(encoding='utf-8', errors='ignore')
        return self.extract_text(content)
    
    def extract_text(self, content):
        try:
            root = ET.fromstring(content)
            return {
                "text": content,
                "format": "xml",
                "root_tag": root.tag,
                "elements": len(list(root.iter()))
            }
        except:
            return {"text": content, "format": "xml", "error": "Invalid XML"}
