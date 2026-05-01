'''Batch Processor — directory-wide file operations.'''
from pathlib import Path
from typing import Dict, List
from .formats import get_metadata, detect_type

def batch_process(directory: str, operation: str = 'info') -> Dict:
    '''Process multiple files in a directory.'''
    dir_path = Path(directory)
    if not dir_path.exists() or not dir_path.is_dir():
        return {'error': f'Directory not found: {directory}'}

    files = [f for f in dir_path.iterdir() if f.is_file()][:50]
    results = []

    for f in files:
        if operation == 'info':
            info = get_metadata(f)
            results.append({'name': f.name, 'type': info.get('type', 'unknown'), 'size': info.get('size_mb', 0)})
        elif operation == 'analyze':
            from .analyzer import analyze_file
            info = analyze_file(str(f), use_ai=True)
            results.append(info)
        elif operation == 'list':
            results.append({'name': f.name, 'path': str(f), 'size': f.stat().st_size})

    return {'directory': str(dir_path), 'total_files': len(files), 'operation': operation, 'processed': len(results), 'results': results}


__all__ = ['batch_process']
