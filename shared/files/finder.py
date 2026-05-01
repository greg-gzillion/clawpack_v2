'''File Finder — search files by name, type, or content.'''
from pathlib import Path
from typing import Dict, List
from .formats import SUPPORTED_FORMATS

def find_files(query: str, search_path: str = None) -> List[Dict]:
    '''Find files by name, type, or content.'''
    search_root = Path(search_path) if search_path else Path.home()
    results = []
    query_lower = query.lower()

    if query_lower.startswith('type:'):
        file_type = query_lower.split(':')[1]
        for category, exts in SUPPORTED_FORMATS.items():
            if file_type in category or file_type in exts:
                for f in search_root.rglob('*'):
                    if f.is_file() and f.suffix.lower() in exts:
                        results.append({'name': f.name, 'path': str(f), 'size': f.stat().st_size, 'type': category})
                        if len(results) >= 20:
                            break
                break
    else:
        for f in search_root.rglob(f'*{query}*'):
            if f.is_file():
                results.append({'name': f.name, 'path': str(f), 'size': f.stat().st_size})
                if len(results) >= 20:
                    break

    return results


__all__ = ['find_files']
