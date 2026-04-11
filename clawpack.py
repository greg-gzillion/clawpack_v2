#!/usr/bin/env python3
"""CLAWPACK - Modular Agent System with Chronicle Search"""
import sys
import asyncio
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.llm_manager import LLMManager
from routes.registry import get_registry

class Clawpack:
    def __init__(self):
        print("\n" + "="*50)
        print("🦞 CLAWPACK v2 - Agentic System")
        print("="*50)
        
        self.llm = LLMManager()
        self.agents = {}
        self.registry = get_registry()
        self._load_agents()
        
        print(f"\n✅ {len(self.agents)} agents | {len(self.llm.llms)} LLMs")
        print("Type /help for commands, /quit to exit")
    
    def _load_agents(self):
        agents_dir = Path("agents")
        for agent_dir in agents_dir.iterdir():
            if not agent_dir.is_dir():
                continue
            if agent_dir.name.startswith('_'):
                continue
            agent_name = agent_dir.name
            agent_file = agent_dir / f"{agent_name}.py"
            if not agent_file.exists():
                agent_file = agent_dir / "agent.py"
            if not agent_file.exists():
                continue
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location(agent_name, agent_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for attr in dir(module):
                    if attr.endswith('Agent') and attr != 'BaseAgent':
                        self.agents[agent_name] = getattr(module, attr)()
                        print(f"  ✅ {agent_name}")
                        break
                else:
                    self.agents[agent_name] = module
                    print(f"  ✅ {agent_name}")
            except Exception as e:
                print(f"  ⚠️ {agent_name}: {str(e)[:50]}")
    
    async def run_async(self):
        while True:
            try:
                cmd = input("\n🦞 > ").strip()
                if not cmd:
                    continue
                
                if cmd in ['/quit', 'quit', 'exit']:
                    print("Goodbye!")
                    break
                if cmd == '/help':
                    print(self.registry.get_all_help())
                    continue
                if cmd == '/llms':
                    print(self.llm.list_models())
                    continue
                if cmd == '/agents':
                    print(f"\nAgents: {', '.join(self.agents.keys())}")
                    continue
                
                # General search using chronicle
                if cmd.startswith("search ") or cmd.startswith("/search "):
                    query = cmd.split(" ", 1)[1].strip()
                    try:
                        from shared.chronicle_helper import search_chronicle
                        results = search_chronicle(query)
                        if results:
                            print(f"\n🦞 SEARCH RESULTS for '{query}':")
                            for card in results[:10]:
                                print(f"  🔗 {card.url}")
                        else:
                            print(f"\n🦞 No results found for '{query}'")
                    except Exception as e:
                        print(f"\n🦞 Search error: {e}")
                    continue
                
                # Chronicle stats
                if cmd == '/chronicle stats':
                    try:
                        from shared.chronicle_helper import get_chronicle_stats
                        stats = get_chronicle_stats()
                        print(f"\n🦞 Chronicle: {stats['total_cards']} cards, {stats['unique_urls']} unique URLs")
                    except Exception as e:
                        print(f"\n🦞 Error: {e}")
                    continue
                
                # Route to agent
                first_word = cmd.split()[0].lower() if cmd else ""
                agent_name = self.registry.get_agent(first_word)
                
                if agent_name in self.agents:
                    agent = self.agents[agent_name]
                    if hasattr(agent, 'handle'):
                        try:
                            result = agent.handle(cmd)
                            print(f"\n🦞 {result}")
                            continue
                        except Exception:
                            pass
                
                # Subprocess fallback
                agent_file = Path(f"agents/{agent_name}/{agent_name}.py")
                if not agent_file.exists():
                    agent_file = Path(f"agents/{agent_name}/agent.py")
                
                if agent_file.exists():
                    result = await asyncio.to_thread(
                        subprocess.run,
                        [sys.executable, str(agent_file), cmd],
                        capture_output=True, text=True, timeout=60
                    )
                    if result.stdout:
                        output = result.stdout.strip()
                        lines = output.split('\n')
                        filtered = [l for l in lines if not l.startswith('🦞') and 'Type' not in l]
                        if filtered:
                            print(f"\n🦞 {'\n'.join(filtered)}")
                else:
                    print(f"\n❌ Unknown command: {first_word}")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def run(self):
        asyncio.run(self.run_async())

if __name__ == "__main__":
    Clawpack().run()
