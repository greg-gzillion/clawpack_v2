"""Memory type definitions - Four-type taxonomy from Claude Code"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

class MemoryType(str, Enum):
    """Four-type taxonomy - only save what cannot be re-derived"""
    USER = "user"           # Who the user is, role, expertise
    FEEDBACK = "feedback"   # Corrections and validations
    PROJECT = "project"     # Ongoing work context
    REFERENCE = "reference" # Pointers to external information

@dataclass
class MemoryFile:
    """Represents a single memory file with frontmatter"""
    name: str
    description: str
    memory_type: MemoryType
    path: str
    created: datetime
    modified: datetime
    staleness_days: int = 0
    
    def is_stale(self, threshold_days: int = 7) -> bool:
        return self.staleness_days > threshold_days
    
    def get_staleness_warning(self) -> str:
        if self.staleness_days == 0:
            return ""
        elif self.staleness_days == 1:
            return "⚠️ This memory is from yesterday. Verify against current code."
        else:
            return f"⚠️ This memory is {self.staleness_days} days old. Code claims may be outdated."

@dataclass
class MemoryManifest:
    """Lightweight manifest for recall - only frontmatter, not full content"""
    files: list[MemoryFile]
    total_count: int
    
    def to_prompt_context(self) -> str:
        """Format manifest for LLM recall selection"""
        lines = ["## Available Memories\n"]
        for f in self.files:
            lines.append(f"- **{f.name}** ({f.memory_type.value}): {f.description}")
        return "\n".join(lines)
