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

# ============================================================================
# A2A Server Command
# ============================================================================

def start_a2a_server(args):
    """Start the A2A protocol server"""
    import subprocess
    import sys
    from pathlib import Path
    
    host = "127.0.0.1"
    port = 8765
    
    # Parse args for custom host/port
    if len(args) > 0:
        host = args[0]
    if len(args) > 1:
        port = int(args[1])
    
    print(f"🦞 Starting Clawpack A2A Server...")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Discovery: http://{host}:{port}/.well-known/agent.json")
    print("")
    print("Press Ctrl+C to stop the server")
    print("")
    
    # Run the server
    server_path = Path(__file__).parent / "agents/webclaw/a2a/integrated_server.py"
    if server_path.exists():
        import subprocess
        subprocess.run([sys.executable, str(server_path)])
    else:
        print("❌ A2A server module not found")

# Add to command router (find where commands are processed)

def smart_route(command):
    """Four-tier routing - inspired by Citadel"""
    # Tier 0: Direct regex matches
    if re.match(r'^fix (typo|spelling|grammar)', command):
        return direct_edit(command)  # 0 tokens
    
    # Tier 1: Active session context
    if command in active_session.commands:
        return session_handler(command)  # 0 tokens
    
    # Tier 2: Keyword lookup
    keywords = extract_keywords(command)
    if matched := keyword_index.get(keywords):
        return matched.handler(command)  # 0 tokens
    
    # Tier 3: LLM classification
    return llm_route(command)  # ~500 tokens

# ============================================================================
# New features integration
# ============================================================================

def dashboard(args):
    """Start web dashboard"""
    import subprocess
    subprocess.Popen([sys.executable, "dashboard/server.py"])
    print("📊 Dashboard started at http://127.0.0.1:3777")

def smart_route_command(args):
    """Use smart routing for commands"""
    from agents.shared.router import smart_router
    command = ' '.join(args)
    result = smart_router.route(command)
    print(f"🎯 Routed to: {result.handler} (Tier {result.tier.value}) - Saved {result.tokens_saved} tokens")
    return result

def decompose_task(args):
    """Decompose complex task"""
    from agents.shared.decomposer import task_decomposer
    task = ' '.join(args)
    subtasks = task_decomposer.decompose(task)
    print(f"📋 Task decomposition for: {task}")
    print(f"📊 Estimated time: {task_decomposer.estimate_time(subtasks)} minutes")
    for i, st in enumerate(subtasks, 1):
        print(f"   {i}. [{st.agent}] {st.name}: {st.description} ({st.estimated_time} min)")
    return subtasks

# Add to command router
def add_new_commands():
    # Add to existing clawpack.py command processing
    pass

# ============================================================================
# New commands from improvements
# ============================================================================

def mcp_command(args):
    """MCP server management"""
    from agents.shared.mcp_registry import mcp_registry
    
    if not args:
        print(mcp_registry.list_servers())
        return
    
    cmd = args[0]
    if cmd == "list":
        print(mcp_registry.list_servers())
    elif cmd == "install" and len(args) > 1:
        print(mcp_registry.install(args[1]))
    elif cmd == "enable" and len(args) > 1:
        print(mcp_registry.enable(args[1]))
    elif cmd == "disable" and len(args) > 1:
        print(mcp_registry.disable(args[1]))
    else:
        print("Usage: mcp [list|install|enable|disable]")

def acp_command(args):
    """ACP agent communication"""
    from agents.shared.acp_client import acp_client
    
    if not args:
        print("Usage: acp <agent> <message>")
        return
    
    agent = args[0]
    message = ' '.join(args[1:]) if len(args) > 1 else ""
    
    if agent in acp_client.SUPPORTED_AGENTS:
        acp_client.agent = agent
        result = acp_client.chat(message)
        print(result)
    else:
        print(f"Unknown agent. Supported: {', '.join(acp_client.SUPPORTED_AGENTS.keys())}")

def sandbox_command(args):
    """Container sandbox management"""
    from agents.shared.sandbox import sandbox
    
    if not args:
        print("Usage: sandbox [create|exec|destroy]")
        return
    
    cmd = args[0]
    if cmd == "create" and len(args) > 1:
        result = sandbox.create(args[1])
        print(f"Sandbox created: {result}")
    elif cmd == "exec" and len(args) > 1:
        result = sandbox.exec_command(' '.join(args[1:]))
        print(result)
    elif cmd == "destroy":
        sandbox.destroy()
        print("Sandbox destroyed")
    else:
        print("Unknown sandbox command")

def budget_command(args):
    """Budget controller status"""
    from agents.shared.budget_controller import budget_controller
    stats = budget_controller.get_stats()
    print(f"💰 Budget Controller: {stats}")

# Add to command router (add these to the existing if/elif chain)
