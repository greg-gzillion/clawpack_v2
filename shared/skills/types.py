"""Skill type definitions"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from pathlib import Path


class SkillSource(str, Enum):
    """Where a skill comes from (priority order)"""
    MANAGED = "managed"       # Enterprise-controlled (highest)
    USER = "user"             # ~/.clawpack/skills/
    PROJECT = "project"       # .clawpack/skills/
    BUILTIN = "builtin"       # Bundled with Clawpack
    MCP = "mcp"               # From MCP server (lowest)


class SkillContext(str, Enum):
    """How the skill should be executed"""
    INLINE = "inline"         # Injected into current conversation
    FORK = "fork"             # Run as sub-agent with own context


@dataclass
class SkillFrontmatter:
    """YAML frontmatter loaded at startup (near-zero token cost)"""
    name: str
    description: str
    source: SkillSource
    path: Path
    
    # Optional fields
    when_to_use: Optional[str] = None      # Detailed usage scenarios
    allowed_tools: List[str] = field(default_factory=list)
    disable_model_invocation: bool = False  # Block autonomous use
    user_invocable: bool = True            # Can user type /skill?
    context: SkillContext = SkillContext.INLINE
    hooks: List[Dict[str, Any]] = field(default_factory=list)
    paths: List[str] = field(default_factory=list)  # Auto-activate on file patterns
    
    # Metadata
    version: Optional[str] = None
    author: Optional[str] = None
    
    def to_prompt_context(self) -> str:
        """Format for system prompt (only frontmatter, not full content)"""
        lines = [f"- **/{self.name}**: {self.description}"]
        if self.when_to_use:
            lines.append(f"  Use when: {self.when_to_use}")
        return '\n'.join(lines)


@dataclass
class Skill:
    """Complete skill with frontmatter and content"""
    frontmatter: SkillFrontmatter
    content: str
    compiled_content: Optional[str] = None  # After variable substitution
    
    def compile(self, variables: Dict[str, str]) -> str:
        """Substitute variables in skill content"""
        content = self.content
        for key, value in variables.items():
            content = content.replace(f'${{{key}}}', str(value))
        
        # Execute inline shell commands (!`command`)
        import re
        import subprocess
        
        def exec_shell(match):
            cmd = match.group(1)
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
                return result.stdout.strip()
            except:
                return f"[Error executing: {cmd}]"
        
        content = re.sub(r'!`([^`]+)`', exec_shell, content)
        
        self.compiled_content = content
        return content


@dataclass
class SkillInvocation:
    """A skill being invoked"""
    skill: Skill
    arguments: str = ""
    variables: Dict[str, str] = field(default_factory=dict)
    invoked_by: str = "user"  # 'user' or 'model'
    
    def get_prompt(self) -> str:
        """Get the full prompt to inject"""
        if not self.skill.compiled_content:
            self.skill.compile(self.variables)
        
        return f"""## Skill: /{self.skill.frontmatter.name}

{self.skill.compiled_content}

---
*Skill invoked with: {self.arguments or 'no arguments'}*
"""
