"""Document Export Module"""
from pathlib import Path
from datetime import datetime

EXPORT_DIR = Path(__file__).parent.parent.parent / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

class ExportHandler:
    @staticmethod
    def to_html(content, name):
        filename = EXPORT_DIR / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filename.write_text(content)
        return filename
    
    @staticmethod
    def to_markdown(content, name):
        filename = EXPORT_DIR / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filename.write_text(content)
        return filename
