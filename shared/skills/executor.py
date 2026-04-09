"""Skill executor - Runs skills with appropriate context"""

import asyncio
from typing import Dict, Any, Optional
from .types import Skill, SkillInvocation, SkillContext


class SkillExecutor:
    """Execute skills with appropriate context"""
    
    def __init__(self, agent):
        self.agent = agent
    
    async def execute(self, invocation: SkillInvocation) -> str:
        """Execute a skill and return the result"""
        if invocation.skill.frontmatter.context == SkillContext.FORK:
            return await self._execute_forked(invocation)
        else:
            return self._execute_inline(invocation)
    
    async def _execute_forked(self, invocation: SkillInvocation) -> str:
        """Run skill as sub-agent with own context"""
        prompt = invocation.get_prompt()
        result = await self.agent.run_subagent(prompt)
        return result
    
    def _execute_inline(self, invocation: SkillInvocation) -> str:
        """Inject skill directly into current conversation"""
        return invocation.get_prompt()
