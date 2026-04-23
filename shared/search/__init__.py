"""Bitmap search for WebClaw - Content indexing with disk persistence"""
import re
import time
import pickle
from pathlib import Path
from typing import List, Dict, Tuple

class SearchResult:
    def __init__(self, path: str, display_name: str, score: float, category: str = "general", preview: str = ""):
        self.path = path
        self.display_name = display_name
        self.score = score
        self.category = category
        self.preview = preview

class BitmapIndex:
    def __init__(self, index_name: str):
        self.index_name = index_name
        self.items = []
        self.index = {}
        self._built = False
        self._build_time_ms = 0
        self._total_items = 0
        self._cache_file = Path(f"agents/webclaw/cache/{index_name}.pkl")
        
        # Try loading from disk immediately
        self._load_from_disk()

    def _load_from_disk(self):
        if self._cache_file.exists():
            try:
                with open(self._cache_file, 'rb') as f:
                    cached = pickle.load(f)
                    self.index = cached['index']
                    self._total_items = cached['total_items']
                    self._build_time_ms = cached['build_time_ms']
                    self._built = True
                    return True
            except:
                pass
        return False

    def add_batch(self, items: List[Tuple[str, str, str]]):
        self.items.extend(items)

    def build(self, force: bool = False):
        if not force and self._built:
            return

        start_time = time.time()
        self.index = {}
        
        for path, display_name, category in self.items:
            try:
                content = Path(path).read_text(encoding='utf-8', errors='ignore')
                text = (display_name + " " + content).lower()
                words = set(re.findall(r'\b[a-z0-9]{3,}\b', text))
                for word in words:
                    if word not in self.index:
                        self.index[word] = []
                    self.index[word].append({
                        'path': path, 'display_name': display_name,
                        'category': category, 'preview': content[:300]
                    })
            except:
                for word in display_name.lower().split():
                    if word not in self.index:
                        self.index[word] = []
                    self.index[word].append({
                        'path': path, 'display_name': display_name,
                        'category': category, 'preview': ""
                    })

        self._built = True
        self._total_items = len(self.items)
        self._build_time_ms = (time.time() - start_time) * 1000
        self._cache_file.parent.mkdir(exist_ok=True)
        with open(self._cache_file, 'wb') as f:
            pickle.dump({'index': self.index, 'total_items': self._total_items, 'build_time_ms': self._build_time_ms}, f)

    def search(self, query: str, max_results: int = 20) -> List[SearchResult]:
        if not self._built:
            self.build()
        query_words = query.lower().split()
        scores = {}
        for word in query_words:
            if word in self.index:
                for item in self.index[word]:
                    key = item['path']
                    scores[key] = scores.get(key, 0) + 1
        sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:max_results]
        return [SearchResult(path=p, display_name="", score=s, category="") for p, s in sorted_items]

    def get_stats(self) -> dict:
        if not self._built:
            self.build()
        return {'total_items': self._total_items, 'build_time_ms': self._build_time_ms, 'index_name': self.index_name, 'unique_words': len(self.index)}

class FuzzyScorer:
    def __init__(self, query: str = ""):
        self.query = query.lower()
    def score(self, text1: str, text2: str) -> float:
        return 1.0 if text1.lower() == text2.lower() else 0.0
    def highlight_matches(self, text: str) -> str:
        return text
