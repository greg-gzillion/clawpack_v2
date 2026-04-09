"""Core memory system - File-based storage with YAML frontmatter"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from .types import MemoryType, MemoryFile, MemoryManifest

class ClawpackMemory:
    """File-based persistent memory for Clawpack agents"""
    
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root).resolve()
        self.memory_dir = self._get_memory_dir()
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.memory_dir / "MEMORY.md"
        self._ensure_index_exists()
    
    def _get_memory_dir(self) -> Path:
        """Get memory directory path - ~/.clawpack/memory/<project-slug>/"""
        home = Path.home()
        slug = self._slugify(str(self.project_root))
        return home / ".clawpack" / "memory" / slug
    
    def _slugify(self, path: str) -> str:
        """Convert path to filesystem-safe slug"""
        # Replace slashes, colons, and special chars with dashes
        slug = re.sub(r'[<>:"|?*\\/]', '-', path)
        # Remove leading/trailing dashes and collapse multiple dashes
        slug = re.sub(r'-+', '-', slug).strip('-')
        return slug or "default"
    
    def _ensure_index_exists(self):
        """Create MEMORY.md index if it doesn't exist"""
        if not self.index_path.exists():
            index_content = """# Clawpack Memory Index

This file is the always-loaded index of all memories for this project.
Each line links to a memory file with a brief description.

## Memory Files

<!-- Memory references will be added here -->

---
*Last updated: {datetime.now().isoformat()}*
"""
            self.index_path.write_text(index_content, encoding='utf-8')
    
    def scan_memory_files(self) -> MemoryManifest:
        """Scan all .md files and extract frontmatter only (first 30 lines)"""
        files = []
        
        for md_file in self.memory_dir.glob("*.md"):
            if md_file.name == "MEMORY.md":
                continue
            
            try:
                content = md_file.read_text(encoding='utf-8')
                frontmatter = self._extract_frontmatter(content)
                
                if frontmatter:
                    mtime = datetime.fromtimestamp(md_file.stat().st_mtime)
                    staleness = (datetime.now() - mtime).days
                    
                    files.append(MemoryFile(
                        name=frontmatter.get('name', md_file.stem),
                        description=frontmatter.get('description', ''),
                        memory_type=MemoryType(frontmatter.get('type', 'feedback')),
                        path=str(md_file),
                        created=datetime.fromtimestamp(md_file.stat().st_ctime),
                        modified=mtime,
                        staleness_days=staleness
                    ))
            except Exception as e:
                print(f"⚠️ Error reading {md_file}: {e}")
        
        return MemoryManifest(files=files, total_count=len(files))
    
    def _extract_frontmatter(self, content: str) -> Optional[Dict[str, Any]]:
        """Extract YAML frontmatter from markdown file"""
        # Match YAML frontmatter between --- markers
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            try:
                return yaml.safe_load(match.group(1))
            except:
                pass
        return None
    
    def recall(self, query: str, max_memories: int = 5) -> List[MemoryFile]:
        """
        Recall relevant memories for a query.
        In production, this would use an LLM side-query.
        For now, uses simple keyword matching.
        """
        manifest = self.scan_memory_files()
        
        if not manifest.files:
            return []
        
        # Simple relevance scoring (placeholder for LLM recall)
        scored = []
        query_lower = query.lower()
        
        for mem in manifest.files:
            score = 0
            if query_lower in mem.name.lower():
                score += 10
            if query_lower in mem.description.lower():
                score += 5
            if mem.memory_type == MemoryType.FEEDBACK:
                score += 2  # Feedback memories are often relevant
            
            if score > 0:
                scored.append((score, mem))
        
        # Sort by score and return top N
        scored.sort(key=lambda x: x[0], reverse=True)
        return [mem for _, mem in scored[:max_memories]]
    
    def record(self, memory_type: MemoryType, name: str, description: str, content: str) -> Path:
        """
        Two-step write protocol:
        1. Create memory file with frontmatter
        2. Update MEMORY.md index
        """
        # Step 1: Create memory file
        filename = f"{memory_type.value}_{self._slugify(name)}.md"
        filepath = self.memory_dir / filename
        
        frontmatter = {
            'name': name,
            'description': description,
            'type': memory_type.value
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
    
    def _update_index(self, name: str, description: str, filename: str):
        """Add one-line reference to MEMORY.md"""
        index_content = self.index_path.read_text(encoding='utf-8')
        
        # Check if already in index
        if f"[{name}]({filename})" not in index_content:
            # Insert before the last update line
            new_line = f"- [{name}]({filename}) -- {description}\n"
            lines = index_content.split('\n')
            
            # Find insertion point (after "## Memory Files")
            for i, line in enumerate(lines):
                if line.strip() == "## Memory Files":
                    lines.insert(i + 2, new_line)
                    break
            
            self.index_path.write_text('\n'.join(lines), encoding='utf-8')
    
    def get_memory_context(self, query: str) -> str:
        """Get formatted memory context for prompt injection"""
        memories = self.recall(query)
        
        if not memories:
            return ""
        
        context = ["## Relevant Memories\n"]
        
        for mem in memories:
            # Read full content
            content = Path(mem.path).read_text(encoding='utf-8')
            
            # Extract body (after frontmatter)
            parts = content.split('---', 2)
            body = parts[2] if len(parts) > 2 else content
            
            context.append(f"### {mem.name} ({mem.memory_type.value})")
            if mem.staleness_days > 0:
                context.append(mem.get_staleness_warning())
            context.append(body[:1000])  # Truncate long memories
            context.append("")
        
        return '\n'.join(context)
