"""Fork manager - Creates and manages forked sub-agents"""

import asyncio
import uuid
import time
from typing import Optional, Dict, Any, List, Callable
from datetime import datetime

from .types import ForkConfig, ForkResult, ForkContext, ForkStatus
from .cache import PromptCache


class ForkManager:
    """
    Manages forked sub-agents with shared prompt cache.
    Forked agents inherit parent's cached prefix (90% token savings).
    """
    
    def __init__(self, parent_agent):
        self.parent = parent_agent
        self.cache = PromptCache()
        self._active_forks: Dict[str, ForkContext] = {}
        self._results: Dict[str, ForkResult] = {}
        self._fork_history: List[ForkResult] = []
    
    def initialize_cache(self, system_prompt: str, tool_definitions: str):
        """Initialize the shared cache with stable content"""
        cacheable_content = f"""{system_prompt}

{tool_definitions}
"""
        self.cache.set_session_prefix(cacheable_content)
    
    async def fork(
        self,
        task: str,
        config: Optional[ForkConfig] = None,
        variables: Optional[Dict[str, Any]] = None
    ) -> ForkResult:
        """
        Fork a new sub-agent to handle a specific task.
        Shares parent's prompt cache for 90% token savings.
        """
        config = config or ForkConfig()
        fork_id = f"fork_{uuid.uuid4().hex[:8]}"
        
        # Create fork context
        context = ForkContext(
            task=task,
            parent_session_id=self.parent.session_id,
            fork_id=fork_id,
            variables=variables or {}
        )
        context.variables['max_turns'] = config.max_turns
        
        self._active_forks[fork_id] = context
        
        start_time = time.time()
        
        try:
            # Build forked prompt (shares parent's cache)
            fork_prompt, cache_hit = self.cache.fork_from_parent(
                context.to_system_prompt()
            )
            
            # Run the forked agent
            result = await self._run_forked_agent(
                context=context,
                prompt=fork_prompt,
                config=config,
                cache_hit=cache_hit
            )
            
            duration_ms = (time.time() - start_time) * 1000
            result.duration_ms = duration_ms
            
        except asyncio.TimeoutError:
            result = ForkResult(
                fork_id=fork_id,
                status=ForkStatus.TIMEOUT,
                error=f"Fork timed out after {config.timeout_seconds}s"
            )
        except Exception as e:
            result = ForkResult(
                fork_id=fork_id,
                status=ForkStatus.FAILED,
                error=str(e)
            )
        
        # Cleanup and store
        self._active_forks.pop(fork_id, None)
        self._results[fork_id] = result
        self._fork_history.append(result)
        
        return result
    
    async def _run_forked_agent(
        self,
        context: ForkContext,
        prompt: str,
        config: ForkConfig,
        cache_hit: bool
    ) -> ForkResult:
        """Run the actual forked agent"""
        
        # Create a lightweight agent instance
        # This would use the same model caller as parent
        turns = 0
        tokens = 0
        tool_calls = []
        final_response = ""
        
        # Simulate agent loop (replace with actual LLM calls)
        messages = [{"role": "user", "content": context.task}]
        
        for turn in range(config.max_turns):
            turns += 1
            
            # This would call the LLM with the forked prompt
            # response = await self.parent.model_caller(messages)
            
            # Mock response for now
            response = f"Forked agent completed task: {context.task[:50]}..."
            final_response = response
            tokens += len(prompt) // 4 + 100
            
            # Check if task is complete
            if "completed" in response.lower() or turn == config.max_turns - 1:
                break
        
        return ForkResult(
            fork_id=context.fork_id,
            status=ForkStatus.COMPLETED,
            result=final_response,
            turns_used=turns,
            tokens_used=tokens,
            cache_hit=cache_hit,
            cache_savings_tokens=self.cache.get_stats()['session_prefix_tokens'] if cache_hit else 0,
            tool_calls=tool_calls
        )
    
    async def fork_many(
        self,
        tasks: List[str],
        config: Optional[ForkConfig] = None,
        max_concurrent: int = 5
    ) -> List[ForkResult]:
        """
        Fork multiple agents in parallel.
        Useful for exploration, code review, etc.
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def fork_one(task: str) -> ForkResult:
            async with semaphore:
                return await self.fork(task, config)
        
        return await asyncio.gather(*[fork_one(t) for t in tasks])
    
    def get_active_forks(self) -> List[str]:
        """Get list of currently active fork IDs"""
        return list(self._active_forks.keys())
    
    def get_result(self, fork_id: str) -> Optional[ForkResult]:
        """Get result of a specific fork"""
        return self._results.get(fork_id)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get fork statistics"""
        cache_stats = self.cache.get_stats()
        return {
            'active_forks': len(self._active_forks),
            'completed_forks': len([r for r in self._fork_history if r.success]),
            'failed_forks': len([r for r in self._fork_history if not r.success]),
            'total_tokens_saved': cache_stats['total_tokens_saved'],
            'estimated_cost_savings': cache_stats['estimated_cost_savings'],
            'recent_forks': [
                {
                    'id': r.fork_id[:8],
                    'status': r.status.value,
                    'turns': r.turns_used,
                    'cache_hit': r.cache_hit
                }
                for r in self._fork_history[-5:]
            ]
        }
    
    def cancel_fork(self, fork_id: str) -> bool:
        """Cancel a running fork"""
        if fork_id in self._active_forks:
            self._active_forks.pop(fork_id)
            self._results[fork_id] = ForkResult(
                fork_id=fork_id,
                status=ForkStatus.CANCELLED,
                error="Cancelled by user"
            )
            return True
        return False
    
    def cancel_all(self) -> int:
        """Cancel all running forks"""
        count = len(self._active_forks)
        for fork_id in list(self._active_forks.keys()):
            self.cancel_fork(fork_id)
        return count
