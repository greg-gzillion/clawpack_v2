'''Shared Files — Imperial Ministry of Documents.

   CONSTITUTIONAL PRINCIPLE: FileClaw is the single authority for all file
   operations. No agent shall handle files directly. All formatting, converting,
   sharing, and file type operations route through this ministry.

   Supported formats: 8 categories, 40+ extensions.
'''
import os
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

SUPPORTED_FORMATS = {
    'document': ['.pdf', '.docx', '.txt', '.md', '.rtf', '.odt', '.html', '.xml'],
    'spreadsheet': ['.csv', '.xlsx', '.xls', '.ods'],
    'image': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp', '.tiff'],
    'code': ['.py', '.js', '.ts', '.rs', '.go', '.cpp', '.c', '.java', '.rb', '.php'],
    'data': ['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg'],
    'archive': ['.zip', '.tar', '.gz', '.bz2', '.7z', '.rar'],
    'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
    'video': ['.mp4', '.mkv', '.avi', '.mov', '.wmv'],
}

# Flattened: extension -> category
EXTENSION_MAP = {}
for category, exts in SUPPORTED_FORMATS.items():
    for ext in exts:
        EXTENSION_MAP[ext] = category


def detect_type(path: Path) -> str:
    '''Detect file type from extension.'''
    return EXTENSION_MAP.get(path.suffix.lower(), 'unknown')


def calculate_hash(path: Path) -> str:
    '''Calculate MD5 hash of first 1MB.'''
    try:
        with open(path, 'rb') as f:
            return hashlib.md5(f.read(1024 * 1024)).hexdigest()
    except Exception:
        return 'N/A'


def get_metadata(path: Path) -> Dict:
    '''Get file metadata without AI analysis.'''
    if not path.exists():
        return {'error': f'File not found: {path}'}
    stat = path.stat()
    return {
        'name': path.name,
        'path': str(path.absolute()),
        'size_bytes': stat.st_size,
        'size_mb': round(stat.st_size / (1024 * 1024), 2),
        'type': detect_type(path),
        'extension': path.suffix,
        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
        'hash': calculate_hash(path),
        'readable': os.access(path, os.R_OK),
        'writable': os.access(path, os.W_OK),
    }


def list_formats() -> Dict[str, List[str]]:
    '''List all supported formats.'''
    return dict(SUPPORTED_FORMATS)


__all__ = ['SUPPORTED_FORMATS', 'EXTENSION_MAP', 'detect_type', 'calculate_hash', 'get_metadata', 'list_formats']
