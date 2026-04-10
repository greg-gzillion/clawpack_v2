"""The Query Loop - Heartbeat of Clawpack with Hooks integration"""
import asyncio
import subprocess
import sys
from pathlib import Path
from typing import AsyncGenerator, List, Dict, Any, Optional

from shared.hooks import HookEvent, HookContext, get_hook_manager

class QueryConfig:
    def __init__(self, max_turns=10, auto_compact=True, permission_mode="default"):
        self.max_turns = max_turns
        self.auto_compact = auto_compact
        self.permission_mode = permission_mode

class QueryLoop:
    def __init__(self, config: QueryConfig, context: Dict[str, Any]):
        self.config = config
        self.context = context
        self.agents_path = Path("agents")
        self.hook_manager = get_hook_manager()
    
    async def query(self, messages: List[Dict]) -> AsyncGenerator[Dict, None]:
        """Execute the agent loop with hooks"""
        if not messages:
            yield {"role": "assistant", "content": "No messages"}
            return
        
        last_msg = messages[-1]
        user_input = last_msg.get("content", "").strip()
        
        # Parse command
        parts = user_input.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        # Get agent name
        agent_name = self._get_agent_for_command(cmd)
        
        if not agent_name:
            agent_name = "mathematicaclaw"
        
        # Create hook context
        hook_context = HookContext(
            event=HookEvent.PRE_TOOL_USE,
            tool_name=cmd,
            tool_input={"command": user_input, "args": args},
            session_id=id(self),
        )
        
        # Run PRE_TOOL_USE hooks
        hook_result = await self.hook_manager.run(HookEvent.PRE_TOOL_USE, hook_context)
        
        # Check if hook blocked
        if hook_result.block:
            yield {"role": "assistant", "content": f"⛔ Blocked: {hook_result.reason}"}
            return
        
        # Use modified input if provided
        final_user_input = user_input
        if hook_result.modified_input:
            final_user_input = hook_result.modified_input.get("command", user_input)
        
        # Add hook context to output if provided
        if hook_result.additional_context:
            yield {"role": "assistant", "content": f"📎 {hook_result.additional_context}"}
        
        # Execute the agent
        result = await self._execute_agent(agent_name, final_user_input)
        
        # Run POST_TOOL_USE hooks
        post_context = HookContext(
            event=HookEvent.POST_TOOL_USE,
            tool_name=cmd,
            tool_input={"command": final_user_input, "result": result},
            session_id=id(self),
        )
        await self.hook_manager.run(HookEvent.POST_TOOL_USE, post_context)
        
        yield {"role": "assistant", "content": result}
    
    def _get_agent_for_command(self, cmd: str) -> Optional[str]:
        """Route command to appropriate agent"""
        # Math commands
        math_commands = ["add", "solve", "plot", "derivative", "diff", "integral", "int", 
                         "simplify", "factor", "expand", "limit", "power", "sqrt", "percent"]
        if cmd in math_commands:
            return "mathematicaclaw"
        
        # Translation
        if cmd in ["translate", "speak"]:
            return "interpretclaw"
        
        # Web search
        if cmd in ["search", "material", "fetch", "browse"]:
            return "webclaw"
        
        # Image generation
        if cmd == "dream":
            return "dreamclaw"
        
        # Legal
        if cmd in ["law", "court", "legal"]:
            return "lawclaw"
        
        # Medical
        if cmd in ["med", "medical"]:
            return "mediclaw"
        
        # Data
        if cmd in ["data", "analyze"]:
            return "dataclaw"
        
        # Language
        if cmd in ["lang", "lesson"]:
            return "langclaw"
        
        # Blockchain
        if cmd == "tx":
            return "txclaw"
        
        # Documents
        if cmd in ["doc", "document"]:
            return "docuclaw"
        
        # Diagrams
        if cmd in ["flow", "flowchart", "diagram"]:
            return "flowclaw"
        
        # Drawing
        if cmd in ["draw", "draft"]:
            return "draftclaw"
        
        # Design
        if cmd == "design":
            return "designclaw"
        
        # Code
        if cmd in ["code", "coder"]:
            return "claw_coder"
        
        # Default to mathematicaclaw
        return "mathematicaclaw"
    
    async def _execute_agent(self, agent_name: str, command: str) -> str:
        """Execute an agent with the given command"""
        agent_file = self.agents_path / agent_name / f"{agent_name}.py"
        
        if not agent_file.exists():
            return f"❌ Agent '{agent_name}' not found"
        
        try:
            # Run the agent in a subprocess
            result = await asyncio.to_thread(
                subprocess.run,
                [sys.executable, str(agent_file), command],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(Path.cwd())
            )
            
            if result.stdout:
                return result.stdout.strip()
            elif result.stderr:
                return f"⚠️ {result.stderr.strip()}"
            else:
                return f"✅ Command executed"
                
        except subprocess.TimeoutExpired:
            return f"⏰ Command timed out after 60 seconds"
        except Exception as e:
            return f"❌ Error: {str(e)}"
