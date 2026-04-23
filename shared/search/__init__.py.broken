"""Bitmap search for WebClaw - Complete implementation"""
import json
import time
from pathlib import Path
from typing import List, Dict, Tuple

class SearchResult:
    def __init__(self, path: str, display_name: str, score: float, category: str = "general"):
        self.path = path
        self.display_name = display_name
        self.score = score
        self.category = category

class BitmapIndex:
    def __init__(self, index_name: str):
        self.index_name = index_name
        self.items = []  # List of (path, display_name, category)
        self.index = {}  # Search index
        self._built = False
        self._build_time_ms = 0
        self._total_items = 0
        
    def add_batch(self, items: List[Tuple[str, str, str]]):
        """Add multiple items to the index"""
        self.items.extend(items)
        
    def build(self):
        """Build the search index"""
        start_time = time.time()
        
        # Create search index from items
        for path, display_name, category in self.items:
            # Index by display name words
            words = display_name.lower().split()
            for word in words:
                if word not in self.index:
                    self.index[word] = []
                self.index[word].append({
                    'path': path,
                    'display_name': display_name,
                    'category': category
                })
        
        self._built = True
        self._total_items = len(self.items)
        self._build_time_ms = (time.time() - start_time) * 1000
        
    def search(self, query: str, max_results: int = 20) -> List[SearchResult]:
        """Search the index and return results"""
        if not self._built:
            self.build()
            
        results = []
        query_words = query.lower().split()
        
        # Score items based on word matches
        scores = {}
        for word in query_words:
            if word in self.index:
                for item in self.index[word]:
                    key = item['path']
                    if key not in scores:
                        scores[key] = {'item': item, 'score': 0}
                    scores[key]['score'] += 1
                    
        # Sort by score and convert to SearchResult
        sorted_items = sorted(scores.items(), key=lambda x: x[1]['score'], reverse=True)
        
        for path, data in sorted_items[:max_results]:
            item = data['item']
            # Calculate normalized score (0-1 range)
            normalized_score = data['score'] / len(query_words) if query_words else 0
            results.append(SearchResult(
                path=path,
                display_name=item['display_name'],
                score=normalized_score,
                category=item['category']
            ))
            
        return results
    
    def get_stats(self) -> dict:
        """Return index statistics"""
        if not self._built:
            self.build()
        return {
            'total_items': self._total_items,
            'build_time_ms': self._build_time_ms,
            'index_name': self.index_name,
            'unique_words': len(self.index)
        }

class FuzzyScorer:
    def __init__(self, query: str = ""):
        self.query = query.lower()
        
    def score(self, text1: str, text2: str) -> float:
        """Simple scoring - 1.0 if exact match, 0.0 otherwise"""
        return 1.0 if text1.lower() == text2.lower() else 0.0
    
    def highlight_matches(self, text: str) -> str:
        """Highlight query matches in text"""
        if not self.query:
            return text
        # Simple highlighting with **
        words = self.query.split()
        result = text
        for word in words:
            import re
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            result = pattern.sub(f"**{word}**", result)
        return result
