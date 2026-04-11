"""Search local indexed content"""

from pathlib import Path
from typing import List, Dict

class LocalSearch:
    def __init__(self, data_root=None):
        self.data_root = Path(data_root) if data_root else Path.cwd() / "data"
    
    def search_files(self, query: str, file_type: str = None) -> List[Dict]:
        """Search local files by name and content"""
        results = []
        
        search_dirs = [self.data_root / file_type] if file_type else self.data_root.iterdir()
        
        for search_dir in search_dirs:
            if not search_dir.exists():
                continue
            
            for file_path in search_dir.rglob('*'):
                if file_path.is_file():
                    if query.lower() in file_path.name.lower():
                        stat = file_path.stat()
                        results.append({
                            'name': file_path.name,
                            'path': str(file_path),
                            'size_mb': round(stat.st_size / (1024 * 1024), 2),
                            'modified': stat.st_mtime
                        })
        
        return results[:20]
    
    def full_text_search(self, query: str, directory: Path = None) -> List[Dict]:
        """Search within file contents for text-based files"""
        results = []
        search_dir = directory or self.data_root
        
        text_extensions = {'.txt', '.md', '.py', '.json', '.csv', '.xml', '.html', '.css', '.js'}
        
        for file_path in search_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in text_extensions:
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    if query.lower() in content.lower():
                        # Find context around match
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if query.lower() in line.lower():
                                results.append({
                                    'file': str(file_path),
                                    'line': i + 1,
                                    'context': line[:200]
                                })
                                break
                except:
                    pass
        
        return results[:20]
