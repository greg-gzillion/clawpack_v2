"""Code analyzer module"""

import re
from pathlib import Path
from typing import Dict, List

class CodeAnalyzer:
    def __init__(self):
        self.clone_pattern = re.compile(r'\.clone\(\)')
    
    def init(self):
        pass
    
    def analyze(self, path: str, analysis_type: str = "stats") -> Dict:
        path_obj = Path(path)
        if not path_obj.exists():
            return {'error': f'Path not found: {path}'}
        
        if analysis_type == "stats":
            return self._stats_analysis(path_obj)
        elif analysis_type == "security":
            return self._security_analysis(path_obj)
        elif analysis_type == "dependencies":
            return self._dependency_analysis(path_obj)
        else:
            return self._complexity_analysis(path_obj)
    
    def _stats_analysis(self, path: Path) -> Dict:
        files = 0
        lines = 0
        for file_path in path.rglob('*.rs'):
            files += 1
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines += len(f.readlines())
            except:
                pass
        return {'files': files, 'lines': lines, 'type': 'stats'}
    
    def _security_analysis(self, path: Path) -> Dict:
        issues = []
        unsafe_patterns = ['unsafe', 'unwrap()', 'expect(', 'panic!']
        
        for file_path in path.rglob('*.rs'):
            try:
                content = file_path.read_text()
                for pattern in unsafe_patterns:
                    if pattern in content:
                        issues.append({'file': str(file_path), 'pattern': pattern})
            except:
                pass
        
        return {'issues': issues, 'count': len(issues), 'type': 'security'}
    
    def _dependency_analysis(self, path: Path) -> Dict:
        deps = []
        cargo_path = path / 'Cargo.toml'
        if cargo_path.exists():
            content = cargo_path.read_text()
            import re
            deps = re.findall(r'([a-zA-Z0-9_-]+)\s*=\s*{[^}]+}', content)
        
        return {'dependencies': deps, 'count': len(deps), 'type': 'dependencies'}
    
    def _complexity_analysis(self, path: Path) -> Dict:
        return {'type': 'complexity', 'message': 'Complexity analysis coming soon'}
    
    def find_unnecessary_clones(self, path: str) -> List[str]:
        path_obj = Path(path)
        results = []
        
        for file_path in path_obj.rglob('*.rs'):
            try:
                content = file_path.read_text()
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if self.clone_pattern.search(line):
                        results.append(f"{file_path}:{i+1}: {line.strip()}")
            except:
                pass
        
        return results
