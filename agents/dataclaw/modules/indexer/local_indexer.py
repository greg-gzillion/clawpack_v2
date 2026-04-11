"""Local indexer"""
class LocalIndexer:
    def __init__(self): pass
    def index_file(self, info): return True
    def index_directory(self, path): return "Indexed"
    def search_local(self, query, limit=10): return []
