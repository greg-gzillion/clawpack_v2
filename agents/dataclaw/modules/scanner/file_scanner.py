"""File scanner"""
class FileScanner:
    SUPPORTED_TYPES = {'documents': ['.pdf', '.txt', '.md']}
    def __init__(self, data_root=None): pass
    def scan_directory(self, path): return []
    def get_file_info(self, path): return {}
    def get_statistics(self): return {'total_files': 0, 'total_size_mb': 0, 'by_type': {}}
