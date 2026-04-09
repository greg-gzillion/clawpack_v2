"""26-bit character bitmap - O(1) pre-filter for search"""

from typing import List, Tuple, Optional
from dataclasses import dataclass
import time

class CharBitmap:
    """
    26-bit bitmap representing which letters (a-z) appear in a string.
    Each bit corresponds to a letter: bit 0 = 'a', bit 1 = 'b', etc.
    """
    
    def __init__(self, text: str = ""):
        self.mask = 0
        if text:
            self.build(text)
    
    def build(self, text: str) -> int:
        """Build bitmap from text - only lowercase a-z"""
        self.mask = 0
        text_lower = text.lower()
        for ch in text_lower:
            code = ord(ch)
            if 97 <= code <= 122:  # 'a' to 'z'
                self.mask |= 1 << (code - 97)
        return self.mask
    
    def contains_all(self, other: 'CharBitmap') -> bool:
        """Check if this bitmap contains all letters from other bitmap"""
        return (self.mask & other.mask) == other.mask
    
    def contains_any(self, other: 'CharBitmap') -> bool:
        """Check if this bitmap shares any letters with other bitmap"""
        return (self.mask & other.mask) != 0
    
    def missing_letters(self, other: 'CharBitmap') -> List[str]:
        """Return which letters from other are missing"""
        missing_mask = other.mask & ~self.mask
        missing = []
        for i in range(26):
            if missing_mask & (1 << i):
                missing.append(chr(97 + i))
        return missing
    
    def __repr__(self) -> str:
        bits = ''.join('1' if self.mask & (1 << i) else '0' for i in range(26))
        return f"CharBitmap(0x{self.mask:08x}, bits={bits})"
    
    def __or__(self, other: 'CharBitmap') -> 'CharBitmap':
        result = CharBitmap()
        result.mask = self.mask | other.mask
        return result
    
    def __and__(self, other: 'CharBitmap') -> 'CharBitmap':
        result = CharBitmap()
        result.mask = self.mask & other.mask
        return result


@dataclass
class IndexedPath:
    """A path with its character bitmap for fast pre-filtering"""
    path: str
    bitmap: CharBitmap
    display_name: str = ""
    category: str = ""
    
    def __post_init__(self):
        if not self.display_name:
            self.display_name = Path(self.path).stem


class BitmapIndex:
    """
    Fast search index using 26-bit character bitmaps.
    
    Pre-filter eliminates candidates that don't contain all query letters.
    Cost: 4 bytes per entry, one integer comparison per candidate.
    Rejection rate: 10-90% depending on query specificity.
    """
    
    def __init__(self, name: str = "index"):
        self.name = name
        self.paths: List[IndexedPath] = []
        self.bitmaps: List[int] = []  # Raw masks for fast iteration
        self._dirty = False
        self._build_time_ms = 0
    
    def add(self, path: str, display_name: str = "", category: str = "") -> None:
        """Add a path to the index"""
        bitmap = CharBitmap(path)
        # Also include display name in bitmap for better matching
        if display_name:
            bitmap.mask |= CharBitmap(display_name).mask
        
        self.paths.append(IndexedPath(
            path=path,
            bitmap=bitmap,
            display_name=display_name or Path(path).stem,
            category=category
        ))
        self.bitmaps.append(bitmap.mask)
        self._dirty = True
    
    def add_batch(self, items: List[Tuple[str, str, str]]) -> None:
        """
        Add multiple items at once.
        Each item: (path, display_name, category)
        """
        for path, display_name, category in items:
            self.add(path, display_name, category)
    
    def build(self) -> None:
        """Finalize index (currently just marks clean)"""
        start = time.perf_counter()
        self._dirty = False
        self._build_time_ms = (time.perf_counter() - start) * 1000
    
    def pre_filter(self, query: str) -> List[int]:
        """
        Fast pre-filter using bitmap.
        Returns indices of paths that contain ALL query letters.
        """
        if not query:
            return list(range(len(self.paths)))
        
        query_bitmap = CharBitmap(query)
        candidates = []
        
        for i, bitmap in enumerate(self.bitmaps):
            # Single integer comparison - extremely fast
            if (bitmap & query_bitmap.mask) == query_bitmap.mask:
                candidates.append(i)
        
        return candidates
    
    def search(self, query: str, max_results: int = 20) -> List[IndexedPath]:
        """
        Full search: pre-filter + scoring.
        """
        # Pre-filter phase (~microseconds)
        candidate_indices = self.pre_filter(query)
        
        if not candidate_indices:
            return []
        
        # Scoring phase - only on filtered candidates
        query_lower = query.lower()
        scored = []
        
        for idx in candidate_indices:
            item = self.paths[idx]
            score = self._score_item(item, query_lower)
            if score > 0:
                scored.append((score, item))
        
        # Sort by score descending
        scored.sort(key=lambda x: x[0], reverse=True)
        
        return [item for _, item in scored[:max_results]]
    
    def _score_item(self, item: IndexedPath, query_lower: str) -> float:
        """Score an item against the query"""
        score = 0.0
        
        # Exact matches in display name
        if query_lower in item.display_name.lower():
            score += 100
        elif query_lower in Path(item.path).stem.lower():
            score += 80
        
        # Partial word matches
        query_words = query_lower.split()
        name_lower = item.display_name.lower()
        path_lower = item.path.lower()
        
        for word in query_words:
            if word in name_lower:
                score += 20
            if word in path_lower:
                score += 10
        
        # Bonus for short names (more likely to be relevant)
        if len(item.display_name) < 30:
            score += 5
        
        # Category bonus
        if item.category:
            if query_lower in item.category.lower():
                score += 15
        
        return score
    
    def get_stats(self) -> dict:
        """Get index statistics"""
        return {
            "name": self.name,
            "total_items": len(self.paths),
            "memory_bytes": len(self.bitmaps) * 4,  # 4 bytes per bitmap
            "build_time_ms": self._build_time_ms,
            "dirty": self._dirty
        }
    
    def clear(self) -> None:
        """Clear the index"""
        self.paths.clear()
        self.bitmaps.clear()
        self._dirty = True


# Import at bottom to avoid circular dependency
from pathlib import Path
