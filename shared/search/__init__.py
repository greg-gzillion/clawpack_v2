"""Bitmap search for WebClaw"""
class BitmapIndex:
    def __init__(self): self.index = {}
    def search(self, query): return []
class FuzzyScorer:
    def score(self, a, b): return 0
class SearchResult:
    def __init__(self, path, score): self.path = path; self.score = score
