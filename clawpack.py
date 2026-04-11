#!/usr/bin/env python3
"""Clawpack V2 - Unified AI Agent Ecosystem"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

class Clawpack:
    def __init__(self):
        self.name = "clawpack"
        self.agents_dir = PROJECT_ROOT / "agents"
        self.agents = {}
        self._load_agents()
        self._print_banner()
    
    def _load_agents(self):
        """Load available agents"""
        agents = {
            "flowclaw": "FlowClaw - Diagram Generator",
            "docuclaw": "DocClaw - Document Processor",
            "txclaw": "TXClaw - Blockchain Assistant",
            "mathematicaclaw": "MathClaw - Mathematics Solver",
            "interpretclaw": "InterpretClaw - Translation",
            "webclaw": "WebClaw - Web Search",
            "dataclaw": "DataClaw - Local References",
            "liberateclaw": "LiberateClaw - Model Liberation",
            "langclaw": "LangClaw - Language Teacher",
            "claw_coder": "ClawCoder - Code Generation",
            "lawclaw": "LawClaw - Legal References",
            "mediclaw": "MedicClaw - Medical References",
            "rustypycraw": "RustyPyCraw - Code Crawler",
        }
        
        for name, desc in agents.items():
            try:
                # Try to import the agent
                agent_path = self.agents_dir / name
                if agent_path.exists():
                    sys.path.insert(0, str(agent_path))
                    module = __import__(name)
                    
                    # Find the agent class
                    agent_class = None
                    for attr in dir(module):
                        if attr.lower() == f"{name}agent" or attr.endswith("Agent"):
                            agent_class = getattr(module, attr)
                            break
                    
                    if agent_class:
                        self.agents[name] = agent_class()
                    else:
                        self.agents[name] = SimpleAgent(name, desc)
                    print(f"  ✅ {name}")
                else:
                    self.agents[name] = SimpleAgent(name, desc)
                    print(f"  ⚠️ {name} (using simple mode)")
            except Exception as e:
                self.agents[name] = SimpleAgent(name, desc)
                print(f"  ⚠️ {name}: {str(e)[:50]}")
    
    def _print_banner(self):
        print("\n" + "="*50)
        print("🦞 CLAWPACK v2 - Agentic System")
        print("="*50)
        print(f"✅ {len(self.agents)} agents loaded")
        print("Type /help for commands, /quit to exit\n")
    
    def run(self):
        """Main REPL loop"""
        while True:
            try:
                cmd = input("🦞 > ").strip()
                if not cmd:
                    continue
                
                if cmd == "/quit" or cmd == "/exit":
                    print("Goodbye!")
                    break
                
                if cmd == "/help":
                    self._show_help()
                    continue
                
                if cmd == "/agents":
                    self._list_agents()
                    continue
                
                # Try to route to appropriate agent
                routed = False
                for name, agent in self.agents.items():
                    if cmd.startswith(f"/{name}"):
                        args = cmd[len(name)+2:].strip()
                        result = agent.handle(args) if hasattr(agent, 'handle') else agent.process("view", args.split())
                        print(result)
                        routed = True
                        break
                
                if not routed:
                    # Default to general response
                    print(f"I understand: {cmd}")
                    print("Try /help for available commands")
            
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def _show_help(self):
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                    CLAWPACK V2 - HELP                            ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  COMMANDS:                                                       ║
║    /help                 - Show this help                       ║
║    /agents               - List all agents                      ║
║    /quit                 - Exit Clawpack                        ║
║                                                                  ║
║  AGENT-SPECIFIC COMMANDS:                                       ║
║    /flowclaw <task>      - Generate diagrams                   ║
║    /docuclaw <task>      - Process documents                   ║
║    /txclaw <task>        - Blockchain operations               ║
║    /liberateclaw <cmd>   - Model liberation                    ║
║                                                                  ║
║  EXAMPLES:                                                       ║
║    /flowclaw view flowchart "user login"                       ║
║    /docuclaw create letter                                      ║
║    /liberateclaw /models                                        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝""")
    
    def _list_agents(self):
        print("\n📋 Available Agents:")
        for name, agent in sorted(self.agents.items()):
            desc = getattr(agent, 'description', 'Ready')
            print(f"  • {name}: {desc}")

class SimpleAgent:
    """Simple fallback agent"""
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def handle(self, query):
        return f"{self.name}: Processing '{query[:100]}'"
    
    def process(self, cmd, args):
        return self.handle(' '.join(args))

def main():
    claw = Clawpack()
    claw.run()

if __name__ == "__main__":
    main()
