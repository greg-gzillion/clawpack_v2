"""CSV importer"""
from pathlib import Path
from importers.base import BaseImporter
import csv
from io import StringIO

class CSVImporter(BaseImporter):
    name = "csv"
    extensions = [".csv", ".tsv"]
    
    def import_file(self, file_path):
        p = Path(file_path)
        content = p.read_text(encoding='utf-8', errors='ignore')
        return self.extract_text(content)
    
    def extract_text(self, content):
        try:
            reader = csv.reader(StringIO(content))
            rows = list(reader)
            return {
                "text": content,
                "format": "csv",
                "rows": len(rows),
                "columns": len(rows[0]) if rows else 0,
                "data": rows  # First 10 rows
            }
        except:
            return {"text": content, "format": "csv", "error": "Invalid CSV"}
