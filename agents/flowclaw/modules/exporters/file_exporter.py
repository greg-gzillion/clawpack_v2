"""File exporter module"""
from pathlib import Path
from datetime import datetime

class FileExporter:
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def save(self, code, diagram_type):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"{diagram_type}_{timestamp}.mmd"
        filename.write_text(code)
        return str(filename)
