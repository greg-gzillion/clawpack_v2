"""Prompt cache sharing for forked agents"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
import hashlib


@dataclass
class SharedPrefix:
    """A shared prompt prefix that can be reused across forks"""
    content: str
    hash_id: str
    token_count: int
    cacheable: bool = True
    
    def __init__(self, content: str, token_count: int = 0):
        self.content = content
        self.hash_id = hashlib.sha256(content.encode()).hexdigest()[:16]
        self.token_count = token_count or self._estimate_tokens(content)
        self.cacheable = True
    
    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation (4 chars ≈ 1 token)"""
        return len(text) // 4


class PromptCache:
    """
    Shared prompt cache for forked agents.
    Parent agent builds cacheable prefix, forks reuse it.
    """
    
    def __init__(self):
        self._prefixes: Dict[str, SharedPrefix] = {}
        self._session_prefix: Optional[SharedPrefix] = None
        self._total_savings: int = 0
        self._fork_count: int = 0
    
    def set_session_prefix(self, content: str):
        """Set the cacheable prefix for this session"""
        self._session_prefix = SharedPrefix(content)
        self._prefixes[self._session_prefix.hash_id] = self._session_prefix
    
    def get_session_prefix(self) -> Optional[SharedPrefix]:
        """Get the current session's cacheable prefix"""
        return self._session_prefix
    
    def fork_from_parent(self, additional_context: str = "") -> Tuple[str, bool]:
        """
        Create a forked prompt that shares the parent's cached prefix.
        Returns (full_prompt, cache_hit_expected)
        """
        self._fork_count += 1
        
        if not self._session_prefix:
            return additional_context, False
        
        # The forked agent's prompt = shared prefix + fork-specific context
        full_prompt = self._session_prefix.content + "\n\n" + additional_context
        
        # Calculate savings
        savings = self._session_prefix.token_count
        self._total_savings += savings
        
        return full_prompt, True
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        return {
            'prefixes_cached': len(self._prefixes),
            'session_prefix_tokens': self._session_prefix.token_count if self._session_prefix else 0,
            'forks_created': self._fork_count,
            'total_tokens_saved': self._total_savings,
            'estimated_cost_savings': f"${self._total_savings * 0.000003:.4f}"  # ~$3/1M tokens
        }
    
    def clear(self):
        """Clear the cache"""
        self._prefixes.clear()
        self._session_prefix = None
        self._total_savings = 0
        self._fork_count = 0
