"""LLM-powered memory recall - Side-query for relevant memories"""

from typing import List, Optional
from .types import MemoryFile, MemoryManifest

class MemoryRecall:
    """LLM-powered recall selector"""
    
    def __init__(self, llm_client=None):
        self.llm = llm_client
    
    def select_relevant(self, query: str, manifest: MemoryManifest, 
                        max_memories: int = 5) -> List[str]:
        """
        Use LLM side-query to select relevant memories.
        
        The prompt instructs the model to:
        - Include only memories useful for current query
        - Skip if uncertain
        - Avoid API docs for tools already in context
        - Surface warnings/gotchas even for known tools
        """
        if not manifest.files or not self.llm:
            return []
        
        prompt = f"""You are selecting relevant memories for an AI agent.

User query: "{query}"

{manifest.to_prompt_context()}

Select up to {max_memories} memories that are RELEVANT to this query.
Return ONLY the filenames (without .md extension), one per line.
Skip memories if uncertain. Avoid API documentation for tools already in context.
BUT surface warnings, gotchas, or known issues.

Relevant memories:"""
        
        try:
            response = self.llm(prompt, max_tokens=256)
            filenames = [line.strip() for line in response.split('\n') 
                        if line.strip() and not line.startswith('#')]
            return filenames[:max_memories]
        except:
            return []
