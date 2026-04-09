"""Two-Phase Skill Loading - Claude Code Pattern #7"""

import yaml
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

class SkillSource(str, Enum):
    MANAGED = "managed"
    USER = "user"
    PROJECT = "project"
    BUILTIN = "builtin"

class SkillContext(str, Enum):
    INLINE = "inline"
    FORK = "fork"

@dataclass
class SkillFrontmatter:
    """Loaded at startup - near-zero token cost"""
    name: str
    description: str
    source: SkillSource
    path: Path
    when_to_use: Optional[str] = None
    allowed_tools: List[str] = field(default_factory=list)
    disable_model_invocation: bool = False
    user_invocable: bool = True
    context: SkillContext = SkillContext.INLINE
    version: Optional[str] = None
    author: Optional[str] = None
    
    def to_prompt_context(self) -> str:
        lines = [f"- **/{self.name}**: {self.description}"]
        if self.when_to_use:
            lines.append(f"  Use when: {self.when_to_use}")
        return '\n'.join(lines)

@dataclass
class Skill:
    """Complete skill with lazy-loaded content"""
    frontmatter: SkillFrontmatter
    _content_path: Path
    _content: Optional[str] = None
    
    @property
    def content(self) -> str:
        """Lazy-load content on first access"""
        if self._content is None:
            self._content = self._content_path.read_text(encoding='utf-8')
        return self._content
    
    def compile(self, variables: Dict[str, str]) -> str:
        """Substitute variables in content"""
        content = self.content
        for key, value in variables.items():
            content = content.replace(f'${{{key}}}', str(value))
        return content

class SkillLoader:
    """Two-phase skill loading"""
    
    def __init__(self):
        self.user_skills_dir = Path.home() / ".clawpack" / "skills"
        self.project_skills_dir = Path.cwd() / ".clawpack" / "skills"
        self.builtin_skills_dir = Path(__file__).parent / "builtin"
    
    def load_all_frontmatter(self) -> List[Skill]:
        """Phase 1: Load only frontmatter at startup"""
        skills = []
        
        sources = [
            (self.builtin_skills_dir, SkillSource.BUILTIN),
            (self.project_skills_dir, SkillSource.PROJECT),
            (self.user_skills_dir, SkillSource.USER),
        ]
        
        for directory, source in sources:
            if directory.exists():
                for skill_dir in directory.iterdir():
                    if not skill_dir.is_dir():
                        continue
                    
                    skill_file = skill_dir / "SKILL.md"
                    if skill_file.exists():
                        skill = self._load_frontmatter_only(skill_file, source, skill_dir)
                        if skill:
                            skills.append(skill)
        
        return skills
    
    def _load_frontmatter_only(self, filepath: Path, source: SkillSource, skill_dir: Path) -> Optional[Skill]:
        """Extract only YAML frontmatter, not full content"""
        content = filepath.read_text(encoding='utf-8')
        
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return None
        
        data = yaml.safe_load(match.group(1)) or {}
        
        frontmatter = SkillFrontmatter(
            name=data.get('name', skill_dir.name),
            description=data.get('description', ''),
            source=source,
            path=skill_dir,
            when_to_use=data.get('when_to_use'),
            allowed_tools=data.get('allowed_tools', []),
            disable_model_invocation=data.get('disable_model_invocation', False),
            user_invocable=data.get('user_invocable', True),
            context=SkillContext(data.get('context', 'inline')),
            version=data.get('version'),
            author=data.get('author')
        )
        
        return Skill(frontmatter=frontmatter, _content_path=filepath)

class SkillManager:
    """Manages skills with two-phase loading"""
    
    def __init__(self):
        self.loader = SkillLoader()
        self._skills: Dict[str, Skill] = {}
        self._load_frontmatter()
    
    def _load_frontmatter(self):
        """Load only frontmatter at startup"""
        skills = self.loader.load_all_frontmatter()
        for skill in skills:
            self._skills[skill.frontmatter.name] = skill
        print(f"📚 Loaded {len(self._skills)} skills (frontmatter only)")
    
    def invoke(self, skill_name: str, arguments: str = "", variables: Dict = None) -> Optional[str]:
        """Phase 2: Load full content on invocation"""
        skill = self._skills.get(skill_name)
        if not skill:
            return None
        
        # Now load the full content
        content = skill.compile(variables or {})
        
        return f"""## Skill: /{skill.frontmatter.name}

{content}

---
*Skill invoked with: {arguments or 'no arguments'}*
"""
    
    def get_prompt_context(self) -> str:
        """Get skill descriptions for system prompt (frontmatter only)"""
        if not self._skills:
            return ""
        
        lines = ["## Available Skills\n"]
        for skill in self._skills.values():
            if skill.frontmatter.user_invocable:
                lines.append(skill.frontmatter.to_prompt_context())
        
        return '\n'.join(lines)
    
    def list_skills(self) -> List[str]:
        return list(self._skills.keys())
