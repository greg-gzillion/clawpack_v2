"""Shared Input Handler - File opening, drag/drop, file picker"""

import os
import sys
from pathlib import Path
from typing import Optional, List

class InputHandler:
    """Universal input handling for all Clawpack agents"""
    
    # Common file locations
    SEARCH_PATHS = [
        Path.cwd(),
        Path.home() / "Downloads",
        Path.home() / "Desktop",
        Path.home() / "Pictures",
        Path.home() / "Documents",
        Path.home() / "OneDrive" / "Pictures",
        Path.home() / "OneDrive" / "Documents",
    ]
    
    # File type categories
    IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff'}
    DOCUMENT_EXTENSIONS = {'.txt', '.md', '.docx', '.pdf', '.html', '.rtf'}
    AUDIO_EXTENSIONS = {'.mp3', '.wav', '.m4a', '.ogg', '.flac'}
    DATA_EXTENSIONS = {'.csv', '.json', '.xml', '.xlsx', '.sql'}
    
    @classmethod
    def find_file(cls, filename: str) -> Optional[Path]:
        """Smart file finder - searches common locations"""
        # Full path
        if Path(filename).exists():
            return Path(filename)
        
        # Search common paths
        for base in cls.SEARCH_PATHS:
            if not base.exists():
                continue
            
            # Exact match
            exact = base / filename
            if exact.exists():
                return exact
            
            # Partial match
            for f in base.glob(f"*{filename}*"):
                return f
            
            # Extension-only search
            if '.' in filename:
                name, ext = filename.rsplit('.', 1)
                for f in base.glob(f"*.{ext}"):
                    if name.lower() in f.stem.lower():
                        return f
        
        return None
    
    @classmethod
    def detect_type(cls, file_path: str) -> str:
        """Detect file type from extension"""
        ext = Path(file_path).suffix.lower()
        if ext in cls.IMAGE_EXTENSIONS:
            return 'image'
        elif ext in cls.DOCUMENT_EXTENSIONS:
            return 'document'
        elif ext in cls.AUDIO_EXTENSIONS:
            return 'audio'
        elif ext in cls.DATA_EXTENSIONS:
            return 'data'
        return 'unknown'
    
    @classmethod
    def open_file(cls, file_path: str) -> bool:
        """Open file with default system application"""
        path = cls.find_file(file_path)
        if path and path.exists():
            os.startfile(str(path))
            return True
        return False
    
    @classmethod
    def list_files(cls, directory: str = None, pattern: str = "*") -> List[Path]:
        """List files in directory"""
        base = Path(directory) if directory else Path.cwd()
        if base.exists():
            return list(base.glob(pattern))
        return []
    
    @classmethod
    def read_text(cls, file_path: str) -> Optional[str]:
        """Read text from file"""
        path = cls.find_file(file_path)
        if path and path.exists():
            return path.read_text(encoding='utf-8')
        return None
    
    @classmethod
    def get_recent_images(cls, limit: int = 10) -> List[Path]:
        """Get recently modified images"""
        images = []
        for base in cls.SEARCH_PATHS:
            if base.exists():
                for ext in cls.IMAGE_EXTENSIONS:
                    for f in base.glob(f"*{ext}"):
                        images.append(f)
        
        # Sort by modification time
        images.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        return images[:limit]


# Convenience functions
def find_file(filename: str) -> Optional[Path]:
    return InputHandler.find_file(filename)

def open_file(file_path: str) -> bool:
    return InputHandler.open_file(file_path)

def detect_type(file_path: str) -> str:
    return InputHandler.detect_type(file_path)
