"""Concurrent-Safe Batching - Claude Code Pattern #3"""

import asyncio
from typing import Dict, List, Callable
from .streaming import ToolSafety

class ToolBatcher:
    """Partition tools by safety, run reads in parallel, serialize writes"""
    
    def __init__(self, safety_map: Dict[str, ToolSafety]):
        self.safety_map = safety_map
    
    def partition(self, tool_calls: List[dict]) -> List[List[dict]]:
        """Group consecutive read-only tools for parallel execution"""
        batches = []
        current = []
        
        for call in tool_calls:
            safety = self.safety_map.get(call["name"], ToolSafety.READ_ONLY)
            
            if safety == ToolSafety.READ_ONLY:
                current.append(call)
            else:
                if current:
                    batches.append(current)
                    current = []
                batches.append([call])  # Write/destructive run alone
        
        if current:
            batches.append(current)
        
        return batches
    
    async def execute_batch(self, batch: List[dict], tools: Dict[str, Callable]) -> List[dict]:
        """Execute a batch - parallel for read-only, serial for writes"""
        if len(batch) == 1:
            call = batch[0]
            func = tools.get(call["name"])
            result = await self._call(func, call.get("args", {}))
            return [{"id": call["id"], "result": result}]
        else:
            # Parallel execution for read-only tools
            tasks = []
            for call in batch:
                func = tools.get(call["name"])
                tasks.append(self._call(func, call.get("args", {})))
            results = await asyncio.gather(*tasks)
            return [{"id": batch[i]["id"], "result": r} for i, r in enumerate(results)]
    
    async def _call(self, func: Callable, args: dict) -> any:
        if asyncio.iscoroutinefunction(func):
            return await func(**args)
        return func(**args)
