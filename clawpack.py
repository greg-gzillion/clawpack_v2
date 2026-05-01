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

                          CLAWPACK V2 - AI AGENT ECOSYSTEM                        

   21 AI Agents     LLM Powered     A2A Ready     Chronicle        
{RESET}
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
            emoji = "" if source == "obliterated" else ""
            return f"{emoji} {model} ({source})"
    return " llama3.2:3b (stock)"

def show_agents():
    """Display available agents"""
    active_model = get_active_model_display()
    print(f"{CYAN}Active Model: {GREEN}{active_model}{RESET}\n")
    
    agents = [
        {"num": 1,  "name": "lawclaw",         "emoji": "⚖️",  "desc": "Law Research & Analysis → DocuClaw, WebClaw"},
        {"num": 2,  "name": "flowclaw",        "emoji": "🔄",  "desc": "Flowcharts & Diagrams → DocuClaw"},
        {"num": 3,  "name": "docuclaw",        "emoji": "📄",  "desc": "Document Creation for ALL agents"},
        {"num": 4,  "name": "mathematicaclaw", "emoji": "📐",  "desc": "Math & Computation → DocuClaw, PlotClaw"},
        {"num": 5,  "name": "liberateclaw",    "emoji": "💥",  "desc": "Model Liberation → Sovereign Gateway"},
        {"num": 6,  "name": "txclaw",          "emoji": "💎",  "desc": "TX Blockchain → DocuClaw, FileClaw"},
        {"num": 7,  "name": "interpretclaw",   "emoji": "🌍",  "desc": "Translation & Speech → WebClaw"},
        {"num": 8,  "name": "langclaw",        "emoji": "🗣️",  "desc": "Language Learning → WebClaw"},
        {"num": 9,  "name": "claw_coder",      "emoji": "💻",  "desc": "Code Generation (39 langs) → DocuClaw"},
        {"num": 10, "name": "dataclaw",        "emoji": "📊",  "desc": "Data Processing → FileClaw"},
        {"num": 11, "name": "webclaw",         "emoji": "🌐",  "desc": "Web Search & References → Chronicle"},
        {"num": 12, "name": "fileclaw",        "emoji": "📁",  "desc": "File Operations (52 formats) → DocuClaw"},
        {"num": 13, "name": "plotclaw",        "emoji": "📈",  "desc": "Charts & Graphs → DocuClaw"},
        {"num": 14, "name": "mediclaw",        "emoji": "🏥",  "desc": "Medical Analysis → DocuClaw, WebClaw"},
        {"num": 15, "name": "dreamclaw",       "emoji": "🎆",  "desc": "AI Vision & Generation → Sov. Gateway"},
        {"num": 16, "name": "designclaw",      "emoji": "🎨",  "desc": "Graphic Design → DocuClaw"},
        {"num": 17, "name": "draftclaw",       "emoji": "✏️",  "desc": "Technical Drawings → DocuClaw"},
        {"num": 18, "name": "crustyclaw",      "emoji": "🦀",  "desc": "Rust AI Assistant → ClawCoder"},
        {"num": 19, "name": "rustypycraw",     "emoji": "🔍",  "desc": "Code Crawler → FileClaw"},
        {"num": 20, "name": "drawclaw",        "emoji": "🖌️",  "desc": "AI Drawing & Art → DocuClaw"},
        {"num": 21, "name": "llmclaw",         "emoji": "🧠",  "desc": "Model Manager → Sovereign Gateway"},
    ]
    
    print("")
    print("                          AVAILABLE AGENTS                             ")
    print("")
    
    for agent in agents:
        print(f" {agent['num']:3}  {agent['emoji']}  {agent['name']:<18} {agent['desc']:<42} ")
    
    print("")
    print("  m    Switch Model                                                   ")
    print("  q    Quit                                                          ")
    print("")

def launch_agent(agent_name):
    """Launch agent via A2A server"""
    import requests
    clear()
    print(f"{GREEN}Connecting to {agent_name} via A2A...{RESET}\n")
    print(f"{CYAN}Type 'exit' to return to menu, 'help' for commands{RESET}\n")
    
    while True:
        try:
            task = input(f"{BOLD}{GREEN}{agent_name}> {RESET}").strip()
            if task.lower() in ("exit", "quit", "q"):
                break
            if not task:
                continue
            
            print(f"{YELLOW}Thinking...{RESET}", end="\r")
            r = requests.post(f"http://127.0.0.1:8766/v1/message/{agent_name}",
                            json={"task": task}, timeout=300)
            if r.status_code == 200:
                data = r.json()
                result = data.get("result", "No response")
                print(" " * 30, end="\r")
                print(result)
            else:
                print(f"{RED}A2A error: {r.status_code}{RESET}")
        except Exception as e:
            if "Connection" in str(e):
                print(f"{RED}A2A server not running. Start with: python a2a_server.py{RESET}")
                input("Press Enter...")
                break
            print(f"{RED}Error: {e}{RESET}")

def launch_model_selector():
    """Launch LLMClaw model selector"""
    clear()
    print(f"{CYAN} LLM Model Selection{RESET}\n")
    
    # Run LLMClaw interface
    subprocess.run([sys.executable, "agents/llmclaw/llmclaw.py"])

def main():
    # First, ensure A2A server is running (optional check)
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_running = sock.connect_ex(('127.0.0.1', 8766)) == 0
    sock.close()
    
    if not server_running:
        print(f"{YELLOW} A2A Server not running on port 8766{RESET}")
        print(f"{YELLOW}   Start with: python a2a_server.py{RESET}")
        input("\nPress Enter to continue anyway...")
    
    while True:
        clear()
        banner()
        show_agents()
        
        choice = input(f"\n{BOLD}{YELLOW} Select agent (1-21), 'm' for model, or 'q' to quit: {RESET}").strip()
        
        if choice.lower() == 'q':
            clear()
            print(f"{GREEN} Goodbye!{RESET}")
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
                17: "draftclaw", 18: "crustyclaw", 19: "rustypycraw",  20: "drawclaw",
                21: "llmclaw"
            }
            
            if num in agents_map:
                launch_agent(agents_map[num])
            else:
                print(f"{RED} Invalid choice{RESET}")
                input("Press Enter...")
        else:
            print(f"{RED} Invalid choice{RESET}")
            input("Press Enter...")

if __name__ == "__main__":
    main()
