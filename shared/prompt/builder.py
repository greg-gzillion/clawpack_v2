"""Cache-stable prompt builder - Stable first, volatile last"""

from dataclasses import dataclass, field
from typing import List, Optional, Callable, Any
from datetime import datetime
from functools import lru_cache
from .cache import CacheStrategy, get_latches

@dataclass
class PromptSection:
    """A section of the prompt with cache strategy"""
    name: str
    content: str
    strategy: CacheStrategy
    order: int = 0
    
    def __post_init__(self):
        if self.strategy == CacheStrategy.STABLE:
            self.order = 0
        elif self.strategy == CacheStrategy.SEMI_STABLE:
            self.order = 1
        elif self.strategy == CacheStrategy.VOLATILE:
            self.order = 2

class PromptBuilder:
    """
    Builds prompts with cache-stable ordering.
    
    Principle: STABLE first, SEMI_STABLE middle, VOLATILE last.
    This maximizes Anthropic's prompt cache hit rate.
    """
    
    def __init__(self, agent_name: str = "clawpack"):
        self.agent_name = agent_name
        self.sections: List[PromptSection] = []
        self._dynamic_boundary_index: Optional[int] = None
        self._session_date = self._get_session_date()
        self.latches = get_latches()
    
    @staticmethod
    @lru_cache(maxsize=1)
    def _get_session_date() -> str:
        """
        Memoized session start date.
        Prevents midnight cache bust - stale date is cosmetic,
        cache bust reprocesses entire conversation.
        """
        return datetime.now().strftime("%Y-%m-%d")
    
    def add_stable(self, name: str, content: str) -> 'PromptBuilder':
        """Add content that NEVER changes - maximum cache sharing"""
        self.sections.append(PromptSection(
            name=name,
            content=content,
            strategy=CacheStrategy.STABLE
        ))
        return self
    
    def add_semi_stable(self, name: str, content: str) -> 'PromptBuilder':
        """Add content that changes rarely - session-level cache"""
        self.sections.append(PromptSection(
            name=name,
            content=content,
            strategy=CacheStrategy.SEMI_STABLE
        ))
        return self
    
    def add_volatile(self, name: str, content: str) -> 'PromptBuilder':
        """Add content that changes every turn - never cached"""
        self.sections.append(PromptSection(
            name=name,
            content=content,
            strategy=CacheStrategy.VOLATILE
        ))
        return self
    
    def add_dynamic_boundary(self) -> 'PromptBuilder':
        """
        Mark the boundary between cached and volatile content.
        Everything before this point is cacheable.
        """
        self._dynamic_boundary_index = len(self.sections)
        return self
    
    def get_system_identity(self) -> str:
        """Stable system identity - same for all agents"""
        return f"""You are Clawpack, an AI agent ecosystem specializing in:
- Language translation (Langclaw)
- Blockchain transactions (TXclaw)
- Medical references (Mediclaw)
- Legal analysis (Lawclaw)
- Mathematical computation (Mathematicaclaw)
- Drawing and visualization (Drawclaw)

Current agent: {self.agent_name}
Session date: {self._session_date}"""
    
    def get_tool_definitions(self, tools: List[dict]) -> str:
        """
        Stable tool definitions - SORTED ALPHABETICALLY.
        Sorting ensures consistent ordering across sessions for cache sharing.
        """
        sorted_tools = sorted(tools, key=lambda t: t.get('name', ''))
        
        lines = ["## Available Tools\n"]
        for tool in sorted_tools:
            lines.append(f"### {tool['name']}")
            lines.append(f"{tool.get('description', 'No description')}")
            if 'parameters' in tool:
                lines.append(f"Parameters: {tool['parameters']}")
            lines.append("")
        
        return '\n'.join(lines)
    
    def get_memory_context(self, memory_context: str) -> str:
        """Semi-stable memory context - changes when memories update"""
        if not memory_context:
            return ""
        return f"## Relevant Memories\n{memory_context}"
    
    def build(self, 
              conversation_history: str,
              current_query: str,
              tool_definitions: Optional[List[dict]] = None,
              memory_context: Optional[str] = None) -> str:
        """
        Build the complete prompt with cache-optimized ordering.
        
        Order:
        1. STABLE: System identity
        2. STABLE: Tool definitions (sorted)
        3. SEMI-STABLE: Memory context
        4. SEMI-STABLE: Project context
        5. VOLATILE: Conversation history
        6. VOLATILE: Current query
        """
        # Reset sections
        self.sections = []
        
        # STABLE LAYER (cached across users with same version)
        self.add_stable("system_identity", self.get_system_identity())
        
        if tool_definitions:
            self.add_stable("tool_definitions", 
                          self.get_tool_definitions(tool_definitions))
        
        # SEMI-STABLE LAYER (cached within session)
        if memory_context:
            self.add_semi_stable("memory_context", memory_context)
        
        # DYNAMIC BOUNDARY - Everything above is cacheable
        self.add_dynamic_boundary()
        
        # VOLATILE LAYER (never cached)
        if conversation_history:
            self.add_volatile("conversation_history", conversation_history)
        
        self.add_volatile("current_query", f"User: {current_query}\n\nAssistant:")
        
        # Sort sections by strategy order
        self.sections.sort(key=lambda s: s.order)
        
        # Build final prompt
        parts = []
        for section in self.sections:
            if section.content:
                parts.append(section.content)
        
        return '\n\n'.join(parts)
    
    def get_cache_stats(self) -> dict:
        """Get statistics about cacheable vs volatile content"""
        stable_chars = sum(len(s.content) for s in self.sections 
                          if s.strategy == CacheStrategy.STABLE)
        semi_chars = sum(len(s.content) for s in self.sections 
                        if s.strategy == CacheStrategy.SEMI_STABLE)
        volatile_chars = sum(len(s.content) for s in self.sections 
                            if s.strategy == CacheStrategy.VOLATILE)
        
        total = stable_chars + semi_chars + volatile_chars
        cacheable = stable_chars + semi_chars
        
        return {
            "total_chars": total,
            "cacheable_chars": cacheable,
            "volatile_chars": volatile_chars,
            "cache_ratio": cacheable / total if total > 0 else 0,
            "estimated_savings": f"{cacheable * 0.00001:.4f} credits"
        }
