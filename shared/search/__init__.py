"""Fast search with bitmap pre-filters - O(1) character presence check"""

from .bitmap import CharBitmap, BitmapIndex
from .scorer import FuzzyScorer, SearchResult

__all__ = ['CharBitmap', 'BitmapIndex', 'FuzzyScorer', 'SearchResult']
