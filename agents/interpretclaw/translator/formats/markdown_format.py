"""Markdown format handler"""

from pathlib import Path
from .base import DocumentFormat

class MarkdownFormat(DocumentFormat):
    """Handler for .md and .markdown files"""
    
    @property
    def supported_extensions(self) -> list:
        return ['.md', '.markdown']
    
    def extract(self, file_path: Path) -> str:
        """Extract text from markdown file"""
        try:
            content = file_path.read_text(encoding='utf-8')
            # Remove markdown syntax for translation
            lines = []
            for line in content.split('\n'):
                if line.startswith('#'):
                    lines.append(line.lstrip('#').strip())
                elif line.startswith('-') or line.startswith('*'):
                    lines.append(line.lstrip('-*').strip())
                else:
                    lines.append(line)
            return '\n'.join(lines)
        except Exception:
            return file_path.read_text(encoding='utf-8', errors='ignore')
    
    def save(self, file_path: Path, content: str, target_lang: str) -> Path:
        """Save translated markdown file"""
        output_path = file_path.parent / f"{file_path.stem}_{target_lang}{file_path.suffix}"
        output_path.write_text(content, encoding='utf-8')
        return output_path
