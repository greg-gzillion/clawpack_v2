"""Extract metadata from various file types"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

class MetadataExtractor:
    """Extract metadata from documents, ebooks, videos, music"""
    
    @staticmethod
    def extract_pdf_metadata(file_path: Path) -> Dict:
        """Extract PDF metadata using PyPDF2"""
        try:
            import PyPDF2
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                info = reader.metadata
                return {
                    'title': info.get('/Title', ''),
                    'author': info.get('/Author', ''),
                    'subject': info.get('/Subject', ''),
                    'pages': len(reader.pages),
                    'producer': info.get('/Producer', ''),
                    'creator': info.get('/Creator', '')
                }
        except:
            return {'error': 'PyPDF2 not installed or PDF reading failed'}
    
    @staticmethod
    def extract_epub_metadata(file_path: Path) -> Dict:
        """Extract EPUB metadata"""
        try:
            import ebooklib
            from ebooklib import epub
            book = epub.read_epub(file_path)
            return {
                'title': book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else '',
                'author': book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else '',
                'language': book.get_metadata('DC', 'language')[0][0] if book.get_metadata('DC', 'language') else '',
                'publisher': book.get_metadata('DC', 'publisher')[0][0] if book.get_metadata('DC', 'publisher') else ''
            }
        except:
            return {'error': 'ebooklib not installed'}
    
    @staticmethod
    def extract_media_metadata(file_path: Path) -> Dict:
        """Extract video/audio metadata using ffprobe"""
        try:
            result = subprocess.run(
                ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', str(file_path)],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return {
                    'duration': float(data.get('format', {}).get('duration', 0)),
                    'size': int(data.get('format', {}).get('size', 0)),
                    'bit_rate': data.get('format', {}).get('bit_rate', ''),
                    'codec': data.get('streams', [{}])[0].get('codec_name', '') if data.get('streams') else ''
                }
        except:
            pass
        return {}
    
    @staticmethod
    def extract_text_content(file_path: Path) -> str:
        """Extract text content from text-based files"""
        try:
            return file_path.read_text(encoding='utf-8', errors='ignore')[:5000]
        except:
            return ""
