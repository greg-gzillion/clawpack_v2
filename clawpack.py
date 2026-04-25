#!/usr/bin/env python3
"""Clawpack V2 - AI Agent Ecosystem with LLM Model Selection"""

import os
import sys
import subprocess
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# ANSI colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(f"""{CYAN}
╔══════════════════════════════════════════════════════════════════════════════╗
║                         🦞 CLAWPACK V2 - AI AGENT ECOSYSTEM                        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  🤖 21 AI Agents  │  🧠 LLM Powered  │  🔗 A2A Ready  │  📚 Chronicle        ║
╚══════════════════════════════════════════════════════════════════════════════╝{RESET}
""")

def get_active_model_display():
    """Show currently active model"""
    import json
    models_dir = Path("models")
    active_file = models_dir / "active_model.json"
    
    if active_file.exists():
        with open(active_file) as f:
            data = json.load(f)
            model = data.get('model', 'none')
            source = data.get('source', 'stock')
            emoji = "🔓" if source == "obliterated" else "📦"
            return f"{emoji} {model} ({source})"
    return "📦 llama3.2:3b (stock)"

def show_agents():
    """Display available agents"""
    active_model = get_active_model_display()
    print(f"{CYAN}Active Model: {GREEN}{active_model}{RESET}\n")
    
    agents = [
        {"num": 1,  "name": "lawclaw",         "emoji": "⚖️",  "desc": "LawClaw Research & AI Case Law"},
        {"num": 2,  "name": "flowclaw",        "emoji": "📊",  "desc": "Flowcharts & Diagrams"},
        {"num": 3,  "name": "docuclaw",        "emoji": "📝",  "desc": "Document Generation"},
        {"num": 4,  "name": "mathematicaclaw", "emoji": "📐",  "desc": "Math & AI Visualization"},
        {"num": 5,  "name": "liberateclaw",    "emoji": "🔓",  "desc": "LLM Model Liberation"},
        {"num": 6,  "name": "txclaw",          "emoji": "💰",  "desc": "TX Blockchain"},
        {"num": 7,  "name": "interpretclaw",   "emoji": "🌐",  "desc": "Translation & Speech"},
        {"num": 8,  "name": "langclaw",        "emoji": "📚",  "desc": "Language Learning"},
        {"num": 9,  "name": "claw_coder",      "emoji": "💻",  "desc": "Code Generation (38 langs)"},
        {"num": 10, "name": "dataclaw",        "emoji": "💾",  "desc": "Data Management"},
        {"num": 11, "name": "webclaw",         "emoji": "🌍",  "desc": "Web Search & Indexing"},
        {"num": 12, "name": "fileclaw",        "emoji": "📁",  "desc": "File Analysis"},
        {"num": 13, "name": "plotclaw",        "emoji": "📈",  "desc": "Charts & Graphs"},
        {"num": 14, "name": "mediclaw",        "emoji": "🏥",  "desc": "Medical References"},
        {"num": 15, "name": "dreamclaw",       "emoji": "🎨",  "desc": "AI Vision & Generation"},
        {"num": 16, "name": "designclaw",      "emoji": "🎯",  "desc": "Graphic Design"},
        {"num": 17, "name": "draftclaw",       "emoji": "📏",  "desc": "Technical Drawings"},
        {"num": 18, "name": "crustyclaw",      "emoji": "🦀",  "desc": "Rust AI Assistant"},
        {"num": 19, "name": "rustypycraw",     "emoji": "🔍",  "desc": "Code Crawler"},
        {"num": 20, "name": "llmclaw",         "emoji": "🧠",  "desc": "LLM Model Manager"},
    ]
    
    print("┌────────────────────────────────────────────────────────────────────────┐")
    print("│                         🤖 AVAILABLE AGENTS                             │")
    print("├────────────────────────────────────────────────────────────────────────┤")
    
    for agent in agents:
        print(f"│ {agent['num']:3}  {agent['emoji']}  {agent['name']:<18} {agent['desc']:<42} │")
    
    print("├────────────────────────────────────────────────────────────────────────┤")
    print("│  m  🧠  Switch Model                                                   │")
    print("│  q  🚪  Quit                                                          │")
    print("└────────────────────────────────────────────────────────────────────────┘")

def launch_agent(agent_name):
    """Launch the selected agent"""
    clear()
    print(f"{GREEN}🦞 Launching {agent_name}...{RESET}\n")
    
    agent_script = Path(f"agents/{agent_name}/{agent_name}.py")
    if agent_script.exists():
        subprocess.run([sys.executable, str(agent_script)])
    else:
        print(f"{RED}❌ Agent not found: {agent_name}{RESET}")
        input("Press Enter...")

def launch_model_selector():
    """Launch LLMClaw model selector"""
    clear()
    print(f"{CYAN}🧠 LLM Model Selection{RESET}\n")
    
    # Run LLMClaw interface
    subprocess.run([sys.executable, "agents/llmclaw/llmclaw.py"])

def main():
    # First, ensure A2A server is running (optional check)
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_running = sock.connect_ex(('127.0.0.1', 8766)) == 0
    sock.close()
    
    if not server_running:
        print(f"{YELLOW}⚠️ A2A Server not running on port 8766{RESET}")
        print(f"{YELLOW}   Start with: python a2a_server.py{RESET}")
        input("\nPress Enter to continue anyway...")
    
    while True:
        clear()
        banner()
        show_agents()
        
        choice = input(f"\n{BOLD}{YELLOW}📋 Select agent (1-20), 'm' for model, or 'q' to quit: {RESET}").strip()
        
        if choice.lower() == 'q':
            clear()
            print(f"{GREEN}👋 Goodbye!{RESET}")
            break
        
        elif choice.lower() == 'm':
            launch_model_selector()
            continue
        
        elif choice.isdigit():
            num = int(choice)
            agents_map = {
                1: "lawclaw", 2: "flowclaw", 3: "docuclaw", 4: "mathematicaclaw",
                5: "liberateclaw", 6: "txclaw", 7: "interpretclaw", 8: "langclaw",
                9: "claw_coder", 10: "dataclaw", 11: "webclaw", 12: "fileclaw",
                13: "plotclaw", 14: "mediclaw", 15: "dreamclaw", 16: "designclaw",
                17: "draftclaw", 18: "crustyclaw", 19: "rustypycraw", 20: "llmclaw"
            }
            
            if num in agents_map:
                launch_agent(agents_map[num])
            else:
                print(f"{RED}❌ Invalid choice{RESET}")
                input("Press Enter...")
        else:
            print(f"{RED}❌ Invalid choice{RESET}")
            input("Press Enter...")

if __name__ == "__main__":
    main()
