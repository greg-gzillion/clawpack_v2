"""4-Layer Context Compression - Claude Code Pattern #5"""

from typing import List, Dict, Any
from dataclasses import dataclass
import re

@dataclass
class CompressionResult:
    """Result of compression operation"""
    original_tokens: int
    compressed_tokens: int
    compression_ratio: float
    layers_applied: List[str]
    content: str

class ContextCompactor:
    """4-layer compression: snip, microcompact, collapse, autocompact"""
    
    def __init__(self, token_limit: int = 200000):
        self.token_limit = token_limit
        self._estimate_tokens = lambda text: len(text) // 4
    
    def compact(self, messages: List[Dict], current_tokens: int) -> CompressionResult:
        """Apply compression layers until under token limit"""
        original_tokens = current_tokens
        layers = []
        
        content = self._messages_to_text(messages)
        
        # Layer 1: Snip - remove redundant tool outputs
        if current_tokens > self.token_limit:
            content = self._snip(content)
            current_tokens = self._estimate_tokens(content)
            layers.append("snip")
        
        # Layer 2: Microcompact - summarize individual messages
        if current_tokens > self.token_limit:
            content = self._microcompact(content)
            current_tokens = self._estimate_tokens(content)
            layers.append("microcompact")
        
        # Layer 3: Collapse - merge similar messages
        if current_tokens > self.token_limit:
            content = self._collapse(content)
            current_tokens = self._estimate_tokens(content)
            layers.append("collapse")
        
        # Layer 4: Autocompact - full conversation summarization
        if current_tokens > self.token_limit:
            content = self._autocompact(content)
            current_tokens = self._estimate_tokens(content)
            layers.append("autocompact")
        
        return CompressionResult(
            original_tokens=original_tokens,
            compressed_tokens=current_tokens,
            compression_ratio=current_tokens / max(1, original_tokens),
            layers_applied=layers,
            content=content
        )
    
    def _messages_to_text(self, messages: List[Dict]) -> str:
        return '\n'.join([m.get('content', '') for m in messages])
    
    def _snip(self, content: str) -> str:
        """Remove duplicate tool outputs and verbose logs"""
        lines = content.split('\n')
        seen = set()
        result = []
        for line in lines:
            if line.startswith('[Tool]'):
                hash_key = hash(line)
                if hash_key in seen:
                    continue
                seen.add(hash_key)
            result.append(line)
        return '\n'.join(result)
    
    def _microcompact(self, content: str) -> str:
        """Summarize individual long messages"""
        lines = content.split('\n')
        result = []
        for line in lines:
            if len(line) > 500:
                result.append(line + "...[truncated]..." + line[-250:])
            else:
                result.append(line)
        return '\n'.join(result)
    
    def _collapse(self, content: str) -> str:
        """Merge similar consecutive messages"""
        lines = content.split('\n')
        result = []
        prev = ""
        for line in lines:
            if line and prev and self._similarity(line, prev) > 0.8:
                result[-1] = prev + " [similar content merged]"
            else:
                result.append(line)
            prev = line
        return '\n'.join(result)
    
    def _similarity(self, a: str, b: str) -> float:
        """Simple similarity check"""
        if not a or not b:
            return 0.0
        a_words = set(a.lower().split())
        b_words = set(b.lower().split())
        if not a_words or not b_words:
            return 0.0
        return len(a_words & b_words) / len(a_words | b_words)
    
    def _autocompact(self, content: str) -> str:
        """Full conversation summarization"""
        # In production, this would call an LLM to summarize
        lines = content.split('\n')
        if len(lines) > 100:
            return f"[Conversation summarized: {len(lines)} lines compressed]\n\n" + \
                   '\n'.join(lines) + "\n...\n" + '\n'.join(lines[-10:])
        return content

# Global instance
_compactor = ContextCompactor()

def get_compactor() -> ContextCompactor:
    return _compactor
