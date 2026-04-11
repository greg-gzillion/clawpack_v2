#!/usr/bin/env python3
"""Clawpack V2 - Unified AI Agent Ecosystem"""

import sys
import os
from pathlib import Path

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
            "lawclaw": "LawClaw - Research",
            "mediclaw": "MedicClaw - Medical References",
            "rustypycraw": "RustyPyCraw - Code Crawler",
        }
        
        for name, desc in agents.items():
            try:
                agent_path = self.agents_dir / name
                if agent_path.exists():
                    sys.path.insert(0, str(agent_path))
                    module = __import__(name)
                    
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
                
                # Route to appropriate agent based on command prefix
                routed = False
                
                # Check for lawclaw commands
                if cmd.startswith("/court") or cmd.startswith("/statute") or cmd.startswith("/case") or cmd.startswith("/search"):
                    if "lawclaw" in self.agents:
                        result = self.agents["lawclaw"].handle(cmd)
                        print(result)
                        routed = True
                
                # Check for liberateclaw commands
                elif cmd.startswith("/liberate") or cmd.startswith("/models") or cmd.startswith("/use"):
                    if "liberateclaw" in self.agents:
                        result = self.agents["liberateclaw"].handle(cmd)
                        print(result)
                        routed = True
                
                # Check for flowclaw commands
                elif cmd.startswith("/flowchart") or cmd.startswith("/diagram"):
                    if "flowclaw" in self.agents:
                        result = self.agents["flowclaw"].handle(cmd)
                        print(result)
                        routed = True
                
                # Check for docuclaw commands
                elif cmd.startswith("/create") or cmd.startswith("/document"):
                    if "docuclaw" in self.agents:
                        result = self.agents["docuclaw"].handle(cmd)
                        print(result)
                        routed = True
                
                # Generic agent command (e.g., /agentname args)
                elif cmd.startswith("/"):
                    parts = cmd[1:].split(maxsplit=1)
                    agent_name = parts[0].lower()
                    if agent_name in self.agents:
                        args = parts[1] if len(parts) > 1 else ""
                        result = self.agents[agent_name].handle(args)
                        print(result)
                        routed = True
                
                if not routed:
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
║  LawClaw COMMANDS:                                      ║
║    /court <code>         - Court information (az, co, federal)  ║
║    /statute <cite>       - Statute lookup                      ║
║    /case <name>          - Case information                    ║
║                                                                  ║
║  MODEL COMMANDS (liberateclaw):                                 ║
║    /models               - List available LLM models           ║
║    /liberate <model>     - Download a model                    ║
║    /use <model> <prompt> - Use a model                         ║
║                                                                  ║
║  OTHER AGENTS:                                                  ║
║    /flowclaw <task>      - Generate diagrams                   ║
║    /docuclaw <task>      - Process documents                   ║
║    /txclaw <task>        - Blockchain operations               ║
║                                                                  ║
║  EXAMPLES:                                                      ║
║    /court az                                                  ║
║    /court co Clear Creek                                     ║
║    /models                                                    ║
║    /liberate tinyllama:1.1b                                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝""")
    
    def _list_agents(self):
        print("\n📋 Available Agents:")
        for name, agent in sorted(self.agents.items()):
            desc = getattr(agent, 'description', 'Ready')
            print(f"  • {name}: {desc}")

class SimpleAgent:
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def handle(self, query):
        return f"{self.name}: Processing '{query[:100]}'"

def main():
    claw = Clawpack()
    claw.run()

if __name__ == "__main__":
    main()
