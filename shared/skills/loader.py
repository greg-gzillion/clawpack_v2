"""Skill loader - Two-phase loading from multiple sources"""

import yaml
import re
from pathlib import Path
from typing import List, Dict, Optional
from .types import Skill, SkillFrontmatter, SkillSource, SkillContext


class SkillLoader:
    """Load skills from all sources with two-phase loading"""
    
    def __init__(self):
        self.user_skills_dir = Path.home() / ".clawpack" / "skills"
        self.project_skills_dir = Path.cwd() / ".clawpack" / "skills"
        self.builtin_skills_dir = Path(__file__).parent / "builtin"
    
    def load_all(self) -> List[Skill]:
        """Load all skills from all sources"""
        all_skills: Dict[str, Skill] = {}
        
        sources = [
            (self.builtin_skills_dir, SkillSource.BUILTIN),
            (self.project_skills_dir, SkillSource.PROJECT),
            (self.user_skills_dir, SkillSource.USER),
        ]
        
        for directory, source in sources:
            if directory.exists():
                for skill in self._load_from_directory(directory, source):
                    if skill.frontmatter.name not in all_skills:
                        all_skills[skill.frontmatter.name] = skill
        
        return list(all_skills.values())
    
    def _load_from_directory(self, directory: Path, source: SkillSource) -> List[Skill]:
        """Load skills from a directory"""
        skills = []
        
        for skill_dir in directory.iterdir():
            if not skill_dir.is_dir():
                continue
            
            skill_file = skill_dir / "SKILL.md"
            if not skill_file.exists():
                continue
            
            try:
                skill = self._load_skill_file(skill_file, source, skill_dir)
                if skill:
                    skills.append(skill)
            except Exception as e:
                print(f"Error loading skill {skill_dir.name}: {e}")
        
        return skills
    
    def _load_skill_file(self, filepath: Path, source: SkillSource, skill_dir: Path) -> Optional[Skill]:
        """Load a single SKILL.md file"""
        content = filepath.read_text(encoding='utf-8')
        
        frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
        if not frontmatter_match:
            return None
        
        frontmatter_yaml = frontmatter_match.group(1)
        body = frontmatter_match.group(2)
        
        data = yaml.safe_load(frontmatter_yaml) or {}
        
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
            hooks=data.get('hooks', []),
            paths=data.get('paths', []),
            version=data.get('version'),
            author=data.get('author')
        )
        
        return Skill(frontmatter=frontmatter, content=body.strip())
    
    def load_by_name(self, name: str) -> Optional[Skill]:
        """Load a specific skill by name"""
        skills = self.load_all()
        for skill in skills:
            if skill.frontmatter.name == name:
                return skill
        return None
