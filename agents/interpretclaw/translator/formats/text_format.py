"""Plain text format handler"""

from pathlib import Path
from .base import DocumentFormat

class TextFormat(DocumentFormat):
    """Handler for .txt files"""
    
    @property
    def supported_extensions(self) -> list:
        return ['.txt']
    
    def extract(self, file_path: Path) -> str:
        """Extract text from plain text file"""
        try:
            return file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            return file_path.read_text(encoding='latin-1')
    
    def save(self, file_path: Path, content: str, target_lang: str) -> Path:
        """Save translated text file"""
        output_path = file_path.parent / f"{file_path.stem}_{target_lang}{file_path.suffix}"
        output_path.write_text(content, encoding='utf-8')
        return output_path
