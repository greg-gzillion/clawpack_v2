"""File-Based Memory System - Claude Code Pattern #6"""

import os
import yaml
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

class MemoryType(str, Enum):
    """Four-type taxonomy from Claude Code"""
    USER = "user"           # Who the user is, role, preferences
    FEEDBACK = "feedback"   # Corrections and validations
    PROJECT = "project"     # Ongoing work context, deadlines
    REFERENCE = "reference" # Pointers to external resources

@dataclass
class MemoryFile:
    """A single memory file with YAML frontmatter"""
    name: str
    description: str
    memory_type: MemoryType
    path: Path
    created: datetime
    modified: datetime
    staleness_days: int = 0
    
    def get_staleness_warning(self) -> str:
        if self.staleness_days == 0:
            return ""
        elif self.staleness_days == 1:
            return "⚠️ This memory is from yesterday. Verify against current code."
        else:
            return f"⚠️ This memory is {self.staleness_days} days old. May be outdated."

class ClawpackMemory:
    """File-based persistent memory with LLM recall"""
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.memory_dir = self._get_memory_dir()
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.memory_dir / "MEMORY.md"
        self._ensure_index()
    
    def _get_memory_dir(self) -> Path:
        """~/.clawpack/memory/<project-slug>/"""
        home = Path.home()
        slug = re.sub(r'[<>:"|?*\\/]', '-', str(self.project_root))
        slug = re.sub(r'-+', '-', slug).strip('-')
        return home / ".clawpack" / "memory" / (slug or "default")
    
    def _ensure_index(self):
        if not self.index_path.exists():
            self.index_path.write_text("""# Clawpack Memory Index

## Memory Files

<!-- Memory references appear here -->

---
*Last updated: {now}*
""".replace('{now}', datetime.now().isoformat()))
    
    def record(self, memory_type: MemoryType, name: str, 
               description: str, content: str) -> Path:
        """Two-step write: create file, update index"""
        # Step 1: Create memory file
        filename = f"{memory_type.value}_{self._slugify(name)}.md"
        filepath = self.memory_dir / filename
        
        frontmatter = {
            'name': name,
            'description': description,
            'type': memory_type.value,
            'created': datetime.now().isoformat()
        }
        
        full_content = f"""---
{yaml.dump(frontmatter)}---
{content}

---
*Recorded: {datetime.now().isoformat()}*
"""
        filepath.write_text(full_content, encoding='utf-8')
        
        # Step 2: Update index
        self._update_index(name, description, filename)
        return filepath
    
    def _slugify(self, text: str) -> str:
        return re.sub(r'[^a-zA-Z0-9_-]', '_', text.lower())[:50]
    
    def _update_index(self, name: str, description: str, filename: str):
        content = self.index_path.read_text()
        if f"[{name}]({filename})" not in content:
            new_line = f"- [{name}]({filename}) -- {description}\n"
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip() == "## Memory Files":
                    lines.insert(i + 2, new_line)
                    break
            self.index_path.write_text('\n'.join(lines))
    
    def recall(self, query: str, max_memories: int = 5) -> List[MemoryFile]:
        """LLM-powered recall - selects relevant memories"""
        manifest = self._scan_memories()
        
        # Simple relevance scoring (replace with LLM side-query for production)
        scored = []
        query_lower = query.lower()
        
        for mem in manifest:
            score = 0
            if query_lower in mem.name.lower():
                score += 10
            if query_lower in mem.description.lower():
                score += 5
            if mem.memory_type == MemoryType.FEEDBACK:
                score += 2
            
            if score > 0:
                scored.append((score, mem))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [mem for _, mem in scored[:max_memories]]
    
    def _scan_memories(self) -> List[MemoryFile]:
        """Scan all .md files and extract frontmatter"""
        memories = []
        for md_file in self.memory_dir.glob("*.md"):
            if md_file.name == "MEMORY.md":
                continue
            
            content = md_file.read_text(encoding='utf-8')
            frontmatter = self._extract_frontmatter(content)
            
            if frontmatter:
                mtime = datetime.fromtimestamp(md_file.stat().st_mtime)
                staleness = (datetime.now() - mtime).days
                
                memories.append(MemoryFile(
                    name=frontmatter.get('name', md_file.stem),
                    description=frontmatter.get('description', ''),
                    memory_type=MemoryType(frontmatter.get('type', 'feedback')),
                    path=md_file,
                    created=datetime.fromisoformat(frontmatter.get('created', datetime.now().isoformat())),
                    modified=mtime,
                    staleness_days=staleness
                ))
        
        return memories
    
    def _extract_frontmatter(self, content: str) -> Optional[Dict]:
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            try:
                return yaml.safe_load(match.group(1))
            except:
                pass
        return None
    
    def get_context(self, query: str) -> str:
        """Get formatted memory context for prompt injection"""
        memories = self.recall(query)
        if not memories:
            return ""
        
        lines = ["## Relevant Memories\n"]
        for mem in memories:
            lines.append(f"### {mem.name} ({mem.memory_type.value})")
            if mem.staleness_days > 0:
                lines.append(mem.get_staleness_warning())
            
            content = mem.path.read_text(encoding='utf-8')
            parts = content.split('---', 2)
            body = parts[2] if len(parts) > 2 else content
            lines.append(body[:500])
            lines.append("")
        
        return '\n'.join(lines)

# Global instance
_memory_instance = None

def get_memory(project_root: Path = None) -> ClawpackMemory:
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = ClawpackMemory(project_root)
    return _memory_instance
