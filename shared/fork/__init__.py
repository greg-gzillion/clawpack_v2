"""Fork Agents - Claude Code Pattern #4"""

import asyncio
import hashlib
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class ForkStatus(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class ForkConfig:
    """Configuration for forked sub-agent"""
    max_turns: int = 25
    max_tokens: int = 50000
    timeout_seconds: int = 300
    inherit_tools: bool = True
    inherit_memory: bool = True
    system_prompt: Optional[str] = None

@dataclass
class ForkResult:
    """Result from a forked agent"""
    fork_id: str
    status: ForkStatus
    result: Optional[str] = None
    error: Optional[str] = None
    turns_used: int = 0
    tokens_used: int = 0
    cache_hit: bool = False
    tokens_saved: int = 0
    duration_ms: float = 0
    
    @property
    def success(self) -> bool:
        return self.status == ForkStatus.COMPLETED

class SharedPrefixCache:
    """Shared prompt cache for forked agents - 90% token savings"""
    
    def __init__(self):
        self._prefixes: Dict[str, str] = {}
        self._session_prefix: Optional[str] = None
        self._total_savings: int = 0
        self._fork_count: int = 0
    
    def set_session_prefix(self, content: str):
        """Set cacheable prefix for this session"""
        self._session_prefix = content
        hash_id = hashlib.sha256(content.encode()).hexdigest()[:16]
        self._prefixes[hash_id] = content
    
    def fork_from_parent(self, task_context: str) -> tuple[str, bool]:
        """Create forked prompt sharing parent's cached prefix"""
        self._fork_count += 1
        
        if not self._session_prefix:
            return task_context, False
        
        full_prompt = self._session_prefix + "\n\n" + task_context
        estimated_tokens = len(self._session_prefix) // 4
        self._total_savings += estimated_tokens
        
        return full_prompt, True
    
    def get_stats(self) -> dict:
        return {
            "prefixes_cached": len(self._prefixes),
            "forks_created": self._fork_count,
            "total_tokens_saved": self._total_savings,
            "estimated_cost_savings": f"${self._total_savings * 0.000003:.4f}"
        }

class ForkManager:
    """Manages forked sub-agents with shared cache"""
    
    def __init__(self, parent_agent):
        self.parent = parent_agent
        self.cache = SharedPrefixCache()
        self._active_forks: Dict[str, Any] = {}
        self._history: List[ForkResult] = []
    
    def initialize_cache(self, system_prompt: str, tool_definitions: str):
        """Initialize shared cache with stable content"""
        cacheable = f"{system_prompt}\n\n{tool_definitions}"
        self.cache.set_session_prefix(cacheable)
    
    async def fork(self, task: str, config: ForkConfig = None) -> ForkResult:
        """Fork a sub-agent for a specific task"""
        config = config or ForkConfig()
        fork_id = f"fork_{uuid.uuid4().hex}"
        
        start_time = datetime.now()
        
        try:
            # Build forked prompt with cache sharing
            prompt, cache_hit = self.cache.fork_from_parent(
                f"## Sub-Agent Task\n{task}\n\nComplete this task and return the result."
            )
            
            # Simulate agent execution (replace with actual LLM call)
            await asyncio.sleep(0.1)
            
            result = ForkResult(
                fork_id=fork_id,
                status=ForkStatus.COMPLETED,
                result=f"[Forked agent completed: {task}...]",
                turns_used=3,
                tokens_used=500,
                cache_hit=cache_hit,
                tokens_saved=len(self.cache._session_prefix) // 4 if cache_hit else 0,
                duration_ms=(datetime.now() - start_time).total_seconds() * 1000
            )
            
        except asyncio.TimeoutError:
            result = ForkResult(
                fork_id=fork_id,
                status=ForkStatus.FAILED,
                error=f"Timeout after {config.timeout_seconds}s"
            )
        except Exception as e:
            result = ForkResult(
                fork_id=fork_id,
                status=ForkStatus.FAILED,
                error=str(e)
            )
        
        self._history.append(result)
        return result
    
    async def fork_many(self, tasks: List[str], max_concurrent: int = 5) -> List[ForkResult]:
        """Fork multiple agents in parallel"""
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def fork_one(task):
            async with semaphore:
                return await self.fork(task)
        
        return await asyncio.gather(*[fork_one(t) for t in tasks])
    
    def get_stats(self) -> dict:
        cache_stats = self.cache.get_stats()
        return {
            **cache_stats,
            "active_forks": len(self._active_forks),
            "completed_forks": len([r for r in self._history if r.success]),
            "failed_forks": len([r for r in self._history if not r.success])
        }
