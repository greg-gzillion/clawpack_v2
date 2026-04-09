"""Fuzzy scoring for search results"""

from dataclasses import dataclass
from typing import List, Optional
import re

@dataclass
class SearchResult:
    """A single search result with score and match info"""
    path: str
    display_name: str
    score: float
    match_positions: List[int] = None
    category: str = ""
    
    def __post_init__(self):
        if self.match_positions is None:
            self.match_positions = []


class FuzzyScorer:
    """
    Advanced scoring for fuzzy search.
    Implements gap penalties and consecutive bonuses.
    """
    
    def __init__(self, query: str):
        self.query = query.lower()
        self.query_chars = list(self.query)
        self.query_length = len(self.query)
    
    def score(self, text: str) -> float:
        """
        Score text against query.
        Returns 0.0-100.0+ with bonuses.
        """
        if not self.query or not text:
            return 0.0
        
        text_lower = text.lower()
        
        # Exact match bonus
        if self.query == text_lower:
            return 200.0
        
        # Prefix match bonus
        if text_lower.startswith(self.query):
            return 100.0 + (50.0 * self.query_length / len(text))
        
        # Word boundary match bonus
        words = re.split(r'[-_./\s]', text_lower)
        for word in words:
            if word.startswith(self.query):
                return 80.0
        
        # Fuzzy match with gap penalties
        positions = self._find_match_positions(text_lower)
        if not positions:
            return 0.0
        
        # Base score from match coverage
        base_score = (len(positions) / self.query_length) * 50.0
        
        # Consecutive bonus
        consecutive = self._count_consecutive(positions)
        consecutive_bonus = consecutive * 10.0
        
        # Gap penalty
        if positions:
            total_span = positions[-1] - positions[0] + 1
            gap_penalty = max(0, (total_span - len(positions)) * 2.0)
        else:
            gap_penalty = 0
        
        # Shorter text bonus (more focused match)
        length_bonus = max(0, 20.0 - len(text) / 5.0)
        
        final_score = base_score + consecutive_bonus - gap_penalty + length_bonus
        
        return max(0.0, final_score)
    
    def _find_match_positions(self, text: str) -> List[int]:
        """Find positions where query characters match in order"""
        positions = []
        text_idx = 0
        
        for q_char in self.query_chars:
            found = False
            while text_idx < len(text):
                if text[text_idx] == q_char:
                    positions.append(text_idx)
                    text_idx += 1
                    found = True
                    break
                text_idx += 1
            
            if not found:
                return []  # Not all characters found
        
        return positions
    
    def _count_consecutive(self, positions: List[int]) -> int:
        """Count consecutive character matches"""
        if len(positions) < 2:
            return 0
        
        consecutive = 0
        for i in range(len(positions) - 1):
            if positions[i + 1] == positions[i] + 1:
                consecutive += 1
        
        return consecutive
    
    def highlight_matches(self, text: str) -> str:
        """Highlight matching characters in text"""
        positions = self._find_match_positions(text.lower())
        if not positions:
            return text
        
        result = []
        last_pos = 0
        for pos in positions:
            result.append(text[last_pos:pos])
            result.append(f"[{text[pos]}]")
            last_pos = pos + 1
        result.append(text[last_pos:])
        
        return ''.join(result)
