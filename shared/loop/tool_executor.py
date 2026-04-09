"""Tool executor with speculative execution and concurrency control"""

import asyncio
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class ToolSafety(str, Enum):
    """Safety classification for concurrent execution"""
    READ_ONLY = "read_only"      # Safe to run in parallel
    WRITE = "write"              # Requires exclusive access
    DESTRUCTIVE = "destructive"  # Requires explicit confirmation


@dataclass
class ToolCall:
    """A pending tool call"""
    id: str
    name: str
    arguments: Dict[str, Any]
    safety: ToolSafety = ToolSafety.READ_ONLY
    
    def to_api_format(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'input': self.arguments
        }


class ToolExecutor:
    """Executes tools with safety-aware concurrency"""
    
    def __init__(self, tools: Dict[str, Callable]):
        self.tools = tools
        self.tool_safety: Dict[str, ToolSafety] = {}
    
    def register_safety(self, tool_name: str, safety: ToolSafety):
        """Register safety classification for a tool"""
        self.tool_safety[tool_name] = safety
    
    def partition_tools(self, tool_calls: List[ToolCall]) -> List[List[ToolCall]]:
        """
        Partition tools into batches for concurrent execution.
        Consecutive READ_ONLY tools can run together.
        WRITE tools run alone.
        """
        batches = []
        current_batch = []
        
        for call in tool_calls:
            safety = self.tool_safety.get(call.name, ToolSafety.READ_ONLY)
            call.safety = safety
            
            if safety == ToolSafety.READ_ONLY:
                current_batch.append(call)
            else:
                # Flush current batch if any
                if current_batch:
                    batches.append(current_batch)
                    current_batch = []
                # Write tools run alone
                batches.append([call])
        
        # Flush remaining
        if current_batch:
            batches.append(current_batch)
        
        return batches
    
    async def execute_batch(self, batch: List[ToolCall]) -> List[Dict]:
        """Execute a batch of tools (possibly in parallel)"""
        if len(batch) == 1:
            # Single tool - execute directly
            call = batch[0]
            result = await self._execute_one(call)
            return [result]
        else:
            # Multiple read-only tools - execute in parallel
            tasks = [self._execute_one(call) for call in batch]
            return await asyncio.gather(*tasks)
    
    async def _execute_one(self, call: ToolCall) -> Dict:
        """Execute a single tool"""
        tool_func = self.tools.get(call.name)
        if not tool_func:
            return {
                'tool_call_id': call.id,
                'error': f"Unknown tool: {call.name}"
            }
        
        try:
            if asyncio.iscoroutinefunction(tool_func):
                result = await tool_func(**call.arguments)
            else:
                result = tool_func(**call.arguments)
            
            return {
                'tool_call_id': call.id,
                'result': result,
                'success': True
            }
        except Exception as e:
            return {
                'tool_call_id': call.id,
                'error': str(e),
                'success': False
            }
    
    async def execute_all(self, tool_calls: List[ToolCall]) -> List[Dict]:
        """Execute all tool calls with optimal batching"""
        batches = self.partition_tools(tool_calls)
        results = []
        
        for batch in batches:
            batch_results = await self.execute_batch(batch)
            results.extend(batch_results)
        
        # Return in original order
        return sorted(results, key=lambda r: tool_calls.index(
            next(c for c in tool_calls if c.id == r['tool_call_id'])
        ))


class StreamingToolExecutor(ToolExecutor):
    """
    Executes tools as they stream in - before model completes response.
    Speculative execution for read-only tools.
    """
    
    def __init__(self, tools: Dict[str, Callable]):
        super().__init__(tools)
        self.pending_calls: List[ToolCall] = []
        self.completed_calls: Dict[str, Dict] = {}
    
    def on_tool_start(self, tool_id: str, tool_name: str):
        """Called when a tool starts streaming"""
        call = ToolCall(
            id=tool_id,
            name=tool_name,
            arguments={},
            safety=self.tool_safety.get(tool_name, ToolSafety.READ_ONLY)
        )
        self.pending_calls.append(call)
    
    def on_tool_arguments(self, tool_id: str, arguments: Dict):
        """Called when tool arguments are complete"""
        for call in self.pending_calls:
            if call.id == tool_id:
                call.arguments = arguments
                break
    
    async def execute_ready(self) -> List[Dict]:
        """
        Execute tools that have complete arguments.
        Read-only tools can execute speculatively before model finishes.
        """
        ready = [c for c in self.pending_calls if c.arguments and c.safety == ToolSafety.READ_ONLY]
        
        if ready:
            results = await self.execute_batch(ready)
            for call in ready:
                self.pending_calls.remove(call)
            return results
        
        return []
    
    async def execute_remaining(self) -> List[Dict]:
        """Execute any remaining pending tools"""
        if not self.pending_calls:
            return []
        
        results = await self.execute_all(self.pending_calls)
        self.pending_calls.clear()
        return results
