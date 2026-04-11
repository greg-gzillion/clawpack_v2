"""Code scanner module"""

import os
from pathlib import Path
from typing import Dict, List

class CodeScanner:
    def __init__(self):
        self.supported_extensions = {
            'rust': ['.rs'],
            'python': ['.py'],
            'typescript': ['.ts', '.tsx'],
            'javascript': ['.js', '.jsx'],
            'solidity': ['.sol'],
            'go': ['.go'],
            'cpp': ['.cpp', '.hpp', '.cc'],
        }
    
    def init(self):
        pass
    
    def scan(self, path: str, language: str = None) -> Dict:
        path_obj = Path(path)
        if not path_obj.exists():
            return {'error': f'Path not found: {path}'}
        
        result = {
            'files': 0,
            'lines': 0,
            'languages': set(),
            'files_by_lang': {}
        }
        
        for ext in self.supported_extensions.get(language, []) if language else sum(self.supported_extensions.values(), []):
            for file_path in path_obj.rglob(f'*{ext}'):
                result['files'] += 1
                lang = self._get_language(ext)
                result['languages'].add(lang)
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = len(f.readlines())
                        result['lines'] += lines
                        result['files_by_lang'][lang] = result['files_by_lang'].get(lang, 0) + 1
                except:
                    pass
        
        result['languages'] = list(result['languages'])
        return result
    
    def _get_language(self, ext: str) -> str:
        for lang, exts in self.supported_extensions.items():
            if ext in exts:
                return lang
        return 'unknown'
