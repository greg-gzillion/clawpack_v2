"""Agent loop - Explicit async generator for complete control flow"""

import asyncio
import time
from typing import AsyncIterator, Optional, List, Dict, Any, Callable
from dataclasses import dataclass, field

from .types import (
    LoopState, TerminalState, TurnResult, 
    LoopResult, StreamChunk
)
from .tool_executor import ToolExecutor, ToolCall


@dataclass
class AgentConfig:
    """Configuration for agent loop"""
    max_turns: int = 50
    max_tokens: int = 200000
    token_warning_threshold: float = 0.8
    stream: bool = True
    temperature: float = 0.7


class AgentLoop:
    """
    Explicit async generator for agent control flow.
    
    One function, one data flow, one place where every interaction passes through.
    This is Claude Code's core architectural bet.
    """
    
    def __init__(
        self,
        model_caller: Callable,
        tools: Dict[str, Callable],
        config: Optional[AgentConfig] = None
    ):
        self.model_caller = model_caller  # Function that calls the LLM
        self.tool_executor = ToolExecutor(tools)
        self.config = config or AgentConfig()
        
        # Session state
        self.messages: List[Dict] = []
        self.turns: List[TurnResult] = []
        self.state = LoopState.IDLE
        self.total_tokens = 0
        self.start_time: Optional[float] = None
    
    async def run(self, user_input: str) -> AsyncIterator[StreamChunk]:
        """
        Main generator loop - yields chunks as they arrive.
        
        Usage:
            async for chunk in agent_loop.run("Hello"):
                if chunk.type == 'text':
                    print(chunk.content, end='')
                elif chunk.type == 'tool_call':
                    print(f"[Executing {chunk.tool_name}...]")
        """
        self.state = LoopState.STREAMING
        self.start_time = time.time()
        
        turn = TurnResult(
            turn_number=len(self.turns) + 1,
            user_input=user_input
        )
        
        # Add user message
        self.messages.append({'role': 'user', 'content': user_input})
        
        try:
            async for chunk in self._run_turn(turn):
                yield chunk
                
                if chunk.type == 'tool_call' and chunk.is_final:
                    turn.tool_calls.append({
                        'id': chunk.tool_id,
                        'name': chunk.tool_name,
                        'arguments': {}  # Would be populated from stream
                    })
                elif chunk.type == 'text':
                    if turn.assistant_output is None:
                        turn.assistant_output = ''
                    turn.assistant_output += chunk.content
            
            # Check termination conditions
            if len(self.turns) >= self.config.max_turns:
                terminal_state = TerminalState.MAX_TURNS
            elif self.total_tokens >= self.config.max_tokens:
                terminal_state = TerminalState.TOKEN_LIMIT
            else:
                terminal_state = TerminalState.COMPLETED
            
        except asyncio.CancelledError:
            terminal_state = TerminalState.CANCELLED
            yield StreamChunk(type='error', content='Cancelled')
        except Exception as e:
            terminal_state = TerminalState.ERROR
            yield StreamChunk(type='error', content=str(e))
        finally:
            self.state = LoopState.IDLE
            self.turns.append(turn)
    
    async def _run_turn(self, turn: TurnResult) -> AsyncIterator[StreamChunk]:
        """Run a single turn of the conversation"""
        
        # Stream model response
        tool_calls = []
        current_text = ""
        current_tool: Optional[Dict] = None
        
        async for chunk in self._stream_model():
            if chunk.type == 'text':
                current_text += chunk.content
                yield chunk
            elif chunk.type == 'tool_call':
                if chunk.tool_name:  # Start of tool call
                    current_tool = {
                        'id': chunk.tool_id,
                        'name': chunk.tool_name,
                        'arguments': {}
                    }
                yield chunk
            elif chunk.type == 'tool_arguments':
                if current_tool:
                    current_tool['arguments'].update(chunk.content)
                yield chunk
            elif chunk.type == 'tool_end':
                if current_tool:
                    tool_calls.append(current_tool)
                    current_tool = None
                yield chunk
        
        # Execute any tool calls
        if tool_calls:
            self.state = LoopState.EXECUTING_TOOLS
            
            # Convert to ToolCall objects
            calls = [
                ToolCall(
                    id=tc['id'],
                    name=tc['name'],
                    arguments=tc['arguments']
                )
                for tc in tool_calls
            ]
            
            # Execute tools
            results = await self.tool_executor.execute_all(calls)
            
            # Add results to messages
            for result in results:
                self.messages.append({
                    'role': 'tool',
                    'tool_call_id': result['tool_call_id'],
                    'content': str(result.get('result', result.get('error', '')))
                })
                turn.tool_results.append(result)
            
            # Continue the loop - model may have more to say
            self.state = LoopState.STREAMING
            async for chunk in self._run_turn(turn):
                yield chunk
    
    async def _stream_model(self) -> AsyncIterator[StreamChunk]:
        """Stream from the model - yields parsed chunks"""
        if not self.config.stream:
            # Non-streaming fallback
            response = await self.model_caller(self.messages)
            yield StreamChunk(
                type='text',
                content=response.get('content', ''),
                is_final=True
            )
            return
        
        # Streaming mode
        async for raw_chunk in self.model_caller(self.messages, stream=True):
            chunk = self._parse_chunk(raw_chunk)
            if chunk:
                if chunk.type == 'text':
                    self.total_tokens += 1  # Approximate
                yield chunk
    
    def _parse_chunk(self, raw: Dict) -> Optional[StreamChunk]:
        """Parse raw API chunk into StreamChunk"""
        # This would parse the actual API response format
        if 'content' in raw:
            return StreamChunk(type='text', content=raw['content'])
        elif 'tool_call' in raw:
            tc = raw['tool_call']
            return StreamChunk(
                type='tool_call',
                content='',
                tool_id=tc.get('id'),
                tool_name=tc.get('name'),
                is_final=tc.get('is_final', False)
            )
        return None
    
    def get_result(self) -> LoopResult:
        """Get final loop result"""
        duration_ms = (time.time() - self.start_time) * 1000 if self.start_time else 0
        
        terminal_state = TerminalState.COMPLETED
        if len(self.turns) >= self.config.max_turns:
            terminal_state = TerminalState.MAX_TURNS
        
        return LoopResult(
            terminal_state=terminal_state,
            turns=self.turns,
            total_tokens=self.total_tokens,
            total_tool_calls=sum(len(t.tool_calls) for t in self.turns),
            duration_ms=duration_ms
        )
    
    def add_message(self, role: str, content: str):
        """Add a message to the conversation history"""
        self.messages.append({'role': role, 'content': content})
    
    def clear_history(self):
        """Clear conversation history"""
        self.messages = []
        self.turns = []
        self.total_tokens = 0


# Convenience function
async def agent_loop(
    user_input: str,
    model_caller: Callable,
    tools: Dict[str, Callable],
    **kwargs
) -> AsyncIterator[StreamChunk]:
    """Convenience function for simple agent loop"""
    loop = AgentLoop(model_caller, tools, AgentConfig(**kwargs))
    async for chunk in loop.run(user_input):
        yield chunk
