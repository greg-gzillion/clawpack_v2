"""File scanner for local media and documents"""

import os
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class FileScanner:
    SUPPORTED_TYPES = {
        'documents': ['.pdf', '.doc', '.docx', '.txt', '.md', '.rtf', '.odt', '.csv', '.xls', '.xlsx'],
        'ebooks': ['.epub', '.mobi', '.azw', '.azw3', '.pdf'],
        'videos': ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
        'music': ['.mp3', '.flac', '.wav', '.aac', '.ogg', '.m4a', '.wma'],
        'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.tiff']
    }
    
    def __init__(self, data_root=None):
        self.data_root = Path(data_root) if data_root else Path.cwd() / "data"
        self.data_root.mkdir(parents=True, exist_ok=True)
    
    def scan_directory(self, directory: Path, recursive=True) -> List[Dict]:
        """Scan a directory for supported files"""
        results = []
        directory = Path(directory)
        
        if not directory.exists():
            return results
        
        pattern = '**/*' if recursive else '*'
        for file_path in directory.glob(pattern):
            if file_path.is_file():
                file_info = self.get_file_info(file_path)
                if file_info:
                    results.append(file_info)
        
        return results
    
    def get_file_info(self, file_path: Path) -> Dict:
        """Get detailed file information"""
        suffix = file_path.suffix.lower()
        
        # Determine file type
        file_type = None
        for type_name, extensions in self.SUPPORTED_TYPES.items():
            if suffix in extensions:
                file_type = type_name
                break
        
        if not file_type:
            return None
        
        stat = file_path.stat()
        
        # Calculate file hash for deduplication
        sha256_hash = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return {
            'name': file_path.name,
            'path': str(file_path.absolute()),
            'type': file_type,
            'extension': suffix,
            'size': stat.st_size,
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'hash': sha256_hash.hexdigest()[:16],
            'parent_dir': str(file_path.parent)
        }
    
    def scan_all_data_dirs(self) -> Dict:
        """Scan all data subdirectories"""
        results = {t: [] for t in self.SUPPORTED_TYPES.keys()}
        
        for type_dir in self.data_root.iterdir():
            if type_dir.is_dir() and type_dir.name in self.SUPPORTED_TYPES:
                files = self.scan_directory(type_dir)
                results[type_dir.name] = files
        
        return results
    
    def get_statistics(self) -> Dict:
        """Get statistics about scanned files"""
        stats = {
            'total_files': 0,
            'total_size_mb': 0,
            'by_type': {}
        }
        
        for type_name in self.SUPPORTED_TYPES.keys():
            type_dir = self.data_root / type_name
            if type_dir.exists():
                files = self.scan_directory(type_dir)
                stats['by_type'][type_name] = {
                    'count': len(files),
                    'size_mb': sum(f['size_mb'] for f in files)
                }
                stats['total_files'] += len(files)
                stats['total_size_mb'] += sum(f['size_mb'] for f in files)
        
        return stats
