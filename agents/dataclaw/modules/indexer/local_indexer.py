"""Local indexer for chronicle integration"""

import sys
from pathlib import Path

CLAWPACK_ROOT = Path("/home/greg/dev/clawpack_v2")
sys.path.insert(0, str(CLAWPACK_ROOT))

class LocalIndexer:
    def __init__(self):
        self.chronicle = None
        self._init_chronicle()
    
    def _init_chronicle(self):
        try:
            from agents.webclaw.core.chronicle_ledger import get_chronicle
            self.chronicle = get_chronicle()
            print("✅ Chronicle connected for local indexing", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ Chronicle error: {e}", file=sys.stderr)
    
    def index_file(self, file_info: dict) -> bool:
        """Index a single file in chronicle"""
        if not self.chronicle:
            return False
        
        try:
            self.chronicle.record_fetch(
                url=f"file://{file_info['path']}",
                context=f"Local {file_info['type']}: {file_info['name']}",
                source=f"dataclaw/{file_info['type']}",
                metadata={
                    'name': file_info['name'],
                    'size_mb': file_info['size_mb'],
                    'type': file_info['type'],
                    'modified': file_info.get('modified', '')
                }
            )
            return True
        except:
            return False
    
    def index_directory(self, directory_path: Path) -> str:
        """Index all files in a directory"""
        if not self.chronicle:
            return "❌ Chronicle not available"
        
        from modules.scanner.file_scanner import FileScanner
        scanner = FileScanner()
        
        files = scanner.scan_directory(directory_path)
        indexed = 0
        for file_info in files:
            if self.index_file(file_info):
                indexed += 1
        
        return f"✅ Indexed {indexed} of {len(files)} files from {directory_path}"
    
    def index_all(self) -> str:
        """Index all data directories"""
        from modules.scanner.file_scanner import FileScanner
        scanner = FileScanner()
        
        results = scanner.scan_all_data_dirs()
        total = 0
        indexed = 0
        
        for file_type, files in results.items():
            total += len(files)
            for file_info in files:
                if self.index_file(file_info):
                    indexed += 1
        
        return f"✅ Indexed {indexed} of {total} files from all data directories"
    
    def search_local(self, query: str, max_results=10) -> list:
        """Search indexed local files"""
        if not self.chronicle:
            return []
        
        try:
            from shared.chronicle_helper import search_chronicle
            results = search_chronicle(f"dataclaw {query}", max_results)
            return [{'url': getattr(r, 'url', str(r)), 'context': getattr(r, 'context', '')} for r in results]
        except:
            return []
