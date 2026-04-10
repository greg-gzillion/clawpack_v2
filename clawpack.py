#!/usr/bin/env python3
"""CLAWPACK - Unified Agent System with QueryLoop"""
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.query import QueryLoop, QueryConfig
from core.agent_loader import AgentLoader
from core.llm_manager import LLMManager

class Clawpack:
    def __init__(self):
        print("\n" + "="*50)
        print("🦞 CLAWPACK v2 - Agentic System")
        print("="*50)
        
        self.loader = AgentLoader()
        self.agents = self.loader.load_all()
        self.llm = LLMManager()
        
        # Create QueryLoop
        self.config = QueryConfig(
            max_turns=10,
            auto_compact=True,
            permission_mode="default"
        )
        self.loop = QueryLoop(self.config, {})
        
        print(f"\n✅ {len(self.agents)} agents | {len(self.llm.llms)} LLMs")
        print("Using QueryLoop generator pattern")
        print("Commands: translate, solve, search, dream, /help, /quit")
    
    async def run_async(self):
        """Run with async generator"""
        messages = []
        
        while True:
            try:
                cmd = input("\n🦞 > ").strip()
                if not cmd:
                    continue
                if cmd == "/quit":
                    break
                if cmd == "/llms":
                    print(self.llm.list_models())
                    continue
                if cmd.startswith("/use "):
                    print(self.llm.select_model(cmd[5:]))
                    continue
                if cmd.startswith("/mode "):
                    mode_str = cmd[6:].strip()
                    mode_map = {
                        "plan": "plan", "default": "default", 
                        "auto": "auto", "bypass": "bypass"
                    }
                    if mode_str in mode_map:
                        self.config.permission_mode = mode_str
                        print(f"🔒 Permission mode: {mode_str}")
                    else:
                        print(f"Unknown mode. Use: plan, default, auto, bypass")
                    continue
                if cmd == "/perms":
                    from shared.permissions import get_permission_system
                    perms = get_permission_system()
                    stats = perms.get_stats()
                    print(f"\n🔒 Permission Stats:")
                    print(f"  Mode: {stats['mode']}")
                    print(f"  Requests: {stats['total_requests']}")
                    print(f"  Allowed: {stats['allowed']}")
                    print(f"  Denied: {stats['denied']}")
                    continue

                    print(self._help())
                    continue
                
                # Add user message
                messages.append({"role": "user", "content": cmd})
                
                # Run query loop
                print(f"\n🤖 Processing...")
                async for message in self.loop.query(messages):
                    if message.get("role") == "assistant":
                        print(f"\n🦞 {message['content']}")
                    elif message.get("tool_result"):
                        print(f"  🔧 {message['tool_result']}")
                
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                break
    
    def run(self):
        """Synchronous wrapper"""
        asyncio.run(self.run_async())
    
    def _help(self):
        return """
🦞 CLAWPACK COMMANDS:
  /llms              - List all LLMs
  /use <model>       - Select model
  /help              - Show this help
  /mode <mode>       - Set permission mode (plan/default/auto/bypass)
  /perms             - Show permission stats
  /quit              - Exit

  translate <text> to <lang>
  speak <text>
  solve <equation>
  search <query>
  dream <prompt>
"""

if __name__ == "__main__":
    Clawpack().run()


