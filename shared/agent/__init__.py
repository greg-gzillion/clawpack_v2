"""Base agent class with all Claude Code patterns integrated"""

import sys
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, AsyncIterator
from abc import ABC, abstractmethod
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.memory import ClawpackMemory, MemoryType
from shared.prompt import PromptBuilder, SlotReservation, get_latches
from shared.search import BitmapIndex
from shared.loop import AgentLoop, AgentConfig, StreamChunk, TerminalState, ToolSafety


class BaseAgent(ABC):
    """
    Base agent with integrated Claude Code patterns:
    - Memory system (file-based + LLM recall)
    - Prompt cache stability (stable first, volatile last)
    - Bitmap search (for references)
    - Generator loop (explicit async generator)
    """
    
    def __init__(self, agent_name: str, project_root: Optional[Path] = None):
        self.agent_name = agent_name
        self.project_root = project_root or Path.cwd()
        
        # Initialize all systems
        self.memory = ClawpackMemory(self.project_root)
        self.prompt_builder = PromptBuilder(agent_name)
        self.slot_reservation = SlotReservation()
        self.latches = get_latches()
        
        # Reference search (for agents with references)
        self.reference_index: Optional[BitmapIndex] = None
        
        # Tools registry
        self.tools: Dict[str, Callable] = {}
        self.tool_safety: Dict[str, ToolSafety] = {}
        
        # Session tracking
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_queries: List[Dict] = []
        
        # Register built-in tools
        self._register_tools()
    
    @abstractmethod
    def _register_tools(self):
        """Register agent-specific tools - override in subclass"""
        pass
    
    def register_tool(self, name: str, func: Callable, safety: ToolSafety = ToolSafety.READ_ONLY):
        """Register a tool with safety classification"""
        self.tools[name] = func
        self.tool_safety[name] = safety
    
    def load_references(self, references_path: Path):
        """Load references into bitmap search index"""
        self.reference_index = BitmapIndex(f"{self.agent_name}_refs")
        
        if references_path.exists():
            items = []
            for md_file in references_path.rglob("*.md"):
                category = md_file.parent.name if md_file.parent != references_path else "general"
                display_name = md_file.stem.replace('_', ' ').replace('-', ' ')
                items.append((str(md_file), display_name, category))
            
            self.reference_index.add_batch(items)
            self.reference_index.build()
            
            stats = self.reference_index.get_stats()
            print(f"   📚 {self.agent_name}: Indexed {stats['total_items']} references")
    
    def search_references(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search agent's reference index"""
        if not self.reference_index:
            return []
        
        results = self.reference_index.search(query, max_results)
        return [
            {
                'path': r.path,
                'name': r.display_name,
                'category': r.category,
                'score': r.score
            }
            for r in results
        ]
    
    def remember(self, memory_type: MemoryType, name: str, description: str, content: str):
        """Record a memory using the file-based system"""
        return self.memory.record(memory_type, name, description, content)
    
    def recall(self, query: str, max_memories: int = 5) -> str:
        """Recall relevant memories for a query"""
        return self.memory.get_memory_context(query)
    
    def build_prompt(self, user_input: str, conversation_history: str = "") -> str:
        """
        Build cache-optimized prompt.
        Stable sections first, volatile last.
        """
        # Get relevant memories
        memory_context = self.recall(user_input)
        
        # Get tool definitions (sorted for cache stability)
        tool_defs = [
            {
                'name': name,
                'description': func.__doc__ or f"Execute {name}",
                'parameters': getattr(func, '__annotations__', {})
            }
            for name, func in self.tools.items()
        ]
        
        return self.prompt_builder.build(
            conversation_history=conversation_history,
            current_query=user_input,
            tool_definitions=tool_defs,
            memory_context=memory_context
        )
    
    async def run(self, user_input: str) -> AsyncIterator[StreamChunk]:
        """
        Run agent with generator loop pattern.
        Yields chunks as they arrive from the model.
        """
        # Build cache-optimized prompt
        prompt = self.build_prompt(user_input)
        
        # Configure agent loop
        config = AgentConfig(
            max_turns=50,
            max_tokens=200000,
            stream=True
        )
        
        # Create loop with model caller
        async def model_caller(messages: list, stream: bool = True):
            # This would call the actual LLM API
            # For now, returns mock response
            async for chunk in self._call_model(prompt, stream):
                yield chunk
        
        loop = AgentLoop(model_caller, self.tools, config)
        
        # Register tool safety
        for name, safety in self.tool_safety.items():
            loop.tool_executor.register_safety(name, safety)
        
        # Run the loop
        async for chunk in loop.run(user_input):
            yield chunk
            
            # Track query
            if chunk.is_final:
                self.session_queries.append({
                    'input': user_input,
                    'timestamp': datetime.now().isoformat(),
                    'chunks': chunk.type
                })
        
        # Get result
        result = loop.get_result()
        
        # Auto-remember important interactions
        if result.was_successful() and len(result.turns) > 2:
            # Record feedback on successful multi-turn interactions
            self.remember(
                MemoryType.FEEDBACK,
                f"Successful {self.agent_name} session",
                f"Completed {len(result.turns)} turns successfully",
                f"User query: {user_input}\nTurns: {len(result.turns)}\nTools used: {result.total_tool_calls}"
            )
    
    async def _call_model(self, prompt: str, stream: bool = True) -> AsyncIterator[Dict]:
        """
        Call the LLM model - override with actual API call.
        This is a placeholder that should be replaced with real API integration.
        """
        # Placeholder - yields mock chunks
        words = prompt.split()[:20]  # Just take first 20 words as mock response
        
        if stream:
            for word in words:
                yield {"content": word + " "}
                await asyncio.sleep(0.05)
        else:
            yield {"content": " ".join(words)}
    
    def get_stats(self) -> Dict:
        """Get session statistics"""
        return {
            'agent': self.agent_name,
            'session_id': self.session_id,
            'queries': len(self.session_queries),
            'tools_registered': len(self.tools),
            'memories': self.memory.scan_memory_files().total_count,
            'references': self.reference_index.get_stats() if self.reference_index else {},
            'prompt_cache': self.prompt_builder.get_cache_stats(),
            'slot_savings': self.slot_reservation.get_savings_estimate()
        }
    
    def list_tools(self) -> List[Dict]:
        """List all registered tools"""
        return [
            {
                'name': name,
                'description': func.__doc__ or 'No description',
                'safety': self.tool_safety.get(name, ToolSafety.READ_ONLY).value
            }
            for name, func in self.tools.items()
        ]


class ClawpackAgentRegistry:
    """Registry for all Clawpack agents"""
    
    _agents: Dict[str, BaseAgent] = {}
    
    @classmethod
    def register(cls, name: str, agent_class: type):
        """Register an agent class"""
        cls._agents[name] = agent_class
    
    @classmethod
    def create(cls, name: str, **kwargs) -> Optional[BaseAgent]:
        """Create an agent instance"""
        agent_class = cls._agents.get(name)
        if agent_class:
            return agent_class(**kwargs)
        return None
    
    @classmethod
    def list_agents(cls) -> List[str]:
        """List all registered agents"""
        return list(cls._agents.keys())


    
    async def _execute_tool_with_hooks(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool with PreToolUse and PostToolUse hooks"""
        
        # PreToolUse hooks
        pre_result = await self.hooks.pre_tool_use(tool_name, arguments)
        
        if pre_result.should_block:
            return {"error": f"Tool blocked by hook: {pre_result.message}"}
        
        if pre_result.has_modifications:
            arguments = pre_result.modified_input
        
        # Execute the actual tool
        tool_func = self.tools.get(tool_name)
        if not tool_func:
            return {"error": f"Unknown tool: {tool_name}"}
        
        try:
            if asyncio.iscoroutinefunction(tool_func):
                result = await tool_func(**arguments)
            else:
                result = tool_func(**arguments)
        except Exception as e:
            # PostToolFailure hooks
            await self.hooks.execute(
                HookPoint.POST_TOOL_FAILURE,
                tool_name=tool_name,
                tool_arguments=arguments,
                tool_error=str(e)
            )
            raise
        
        # PostToolUse hooks
        post_result = await self.hooks.post_tool_use(tool_name, arguments, result)
        
        if post_result.additional_context:
            if isinstance(result, dict):
                result['_hook_context'] = post_result.additional_context
        
        return result
