"""Skill manager - Main interface for skills system"""

from typing import List, Optional, Dict
from .types import Skill, SkillInvocation
from .loader import SkillLoader
from .executor import SkillExecutor


class SkillManager:
    """Central manager for the skills system"""
    
    def __init__(self, agent):
        self.agent = agent
        self.loader = SkillLoader()
        self.executor = SkillExecutor(agent)
        self._skills: Dict[str, Skill] = {}
        self._load_skills()
    
    def _load_skills(self):
        """Load all skills at startup (frontmatter only)"""
        skills = self.loader.load_all()
        for skill in skills:
            self._skills[skill.frontmatter.name] = skill
        print(f"📚 Loaded {len(self._skills)} skills")
    
    def list_skills(self) -> List[str]:
        """List all available skill names"""
        return list(self._skills.keys())
    
    def get_skill(self, name: str) -> Optional[Skill]:
        """Get a skill by name"""
        return self._skills.get(name)
    
    async def invoke(self, skill_name: str, arguments: str = "", 
                     variables: Dict[str, str] = None) -> Optional[str]:
        """Invoke a skill by name"""
        skill = self.get_skill(skill_name)
        if not skill:
            return None
        
        invocation = SkillInvocation(
            skill=skill,
            arguments=arguments,
            variables=variables or {}
        )
        
        return await self.executor.execute(invocation)
    
    def get_prompt_context(self) -> str:
        """Get skill descriptions for system prompt"""
        if not self._skills:
            return ""
        
        lines = ["## Available Skills\n"]
        for skill in self._skills.values():
            if skill.frontmatter.user_invocable:
                lines.append(skill.frontmatter.to_prompt_context())
        
        return '\n'.join(lines)
    
    def create_examples(self):
        """Create example skills"""
        self.loader.create_example_skills()
        self._load_skills()
