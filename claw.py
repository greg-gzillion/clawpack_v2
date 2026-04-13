#!/usr/bin/env python3
"""Clawpack Agent Selection Menu - Stays Open"""

import sys
import subprocess
from pathlib import Path
import json

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

def clear():
    import os
    os.system('clear' if os.name == 'posix' else 'cls')

def get_active_model():
    state_file = Path("models/active_model.json")
    if state_file.exists():
        with open(state_file) as f:
            data = json.load(f)
            return data.get("model"), data.get("source")
    return None, None

def show_banner():
    model, source = get_active_model()
    print(f"{CYAN}╔══════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║              🦞 CLAWPACK - AI AGENT LAUNCHER                   ║{RESET}")
    print(f"{CYAN}╠══════════════════════════════════════════════════════════════╣{RESET}")
    if model:
        source_display = "🔓 Obliterated" if source == "obliterated" else "📦 Stock"
        print(f"{CYAN}║  Active: {GREEN}{model}{CYAN} ({source_display}){' ' * (42 - len(model) - len(source_display))}║{RESET}")
    else:
        print(f"{CYAN}║  {RED}No model selected{RESET}{' ' * 42}║{RESET}")
    print(f"{CYAN}╚══════════════════════════════════════════════════════════════╝{RESET}")

def discover_agents():
    agents_dir = Path("agents")
    agents = {}
    for agent_dir in agents_dir.iterdir():
        if not agent_dir.is_dir():
            continue
        if agent_dir.name.startswith(('_', 'shared', 'langclaw_backup')):
            continue
        agent_file = agent_dir / f"{agent_dir.name}.py"
        if agent_file.exists():
            name = agent_dir.name.replace('claw', '')
            if not name:
                name = agent_dir.name
            agents[name] = str(agent_file)
    return agents

def run_agent(agent_path, args=None):
    if args is None:
        args = []
    model, source = get_active_model()
    env = subprocess.os.environ.copy()
    if model:
        env['CLAWPACK_MODEL'] = model
        env['CLAWPACK_SOURCE'] = source or 'stock'
    cmd = [sys.executable, agent_path] + args
    subprocess.run(cmd, env=env)

def main():
    AGENTS = discover_agents()
    
    while True:
        clear()
        show_banner()
        
        print(f"\n{YELLOW}Available Agents:{RESET}\n")
        
        categories = {
            "🦞 MODEL": ["llm"],
            "⚖️ LEGAL": ["law"],
            "🏥 MEDICAL": ["med"],
            "💻 CODE": ["_coder", "rusty"],
            "📊 DATA": ["data", "web", "docu", "file"],
            "🎨 CREATIVE": ["design", "draw", "draft", "dream", "plot", "flow"],
            "🌐 LANGUAGE": ["lang", "interpret"],
            "💰 BLOCKCHAIN": ["tx"],
            "🔧 SYSTEM": ["liberate"]
        }
        
        agent_list = []
        idx = 1
        for cat, patterns in categories.items():
            shown = False
            for name in sorted(AGENTS.keys()):
                if any(p in name for p in patterns):
                    if not shown:
                        print(f"\n{GREEN}{cat}:{RESET}")
                        shown = True
                    print(f"  [{idx:2}] {name:12} → {Path(AGENTS[name]).parent.name}")
                    agent_list.append((name, AGENTS[name]))
                    idx += 1
        
        print(f"\n  {'─' * 50}")
        print(f"  [m] 🦞 Change Model (LLMClaw)")
        print(f"  [q] 🚪 Quit")
        print(f"  {'─' * 50}")
        
        choice = input(f"\n{BOLD}{YELLOW}📋 Select agent (1-{len(agent_list)}), 'm', or 'q': {RESET}").strip().lower()
        
        if choice == 'q':
            clear()
            print(f"{GREEN}👋 Goodbye!{RESET}")
            break
        elif choice == 'm':
            print(f"\n{GREEN}🦞 Launching LLMClaw...{RESET}")
            subprocess.run([sys.executable, "agents/llmclaw/llmclaw.py"])
            continue
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(agent_list):
                agent_name, agent_path = agent_list[idx]
                print(f"\n{GREEN}🚀 Launching {agent_name}...{RESET}")
                print(f"{YELLOW}Type 'back' to return to menu{RESET}\n")
                
                # Run agent interactively
                if agent_name == "llm":
                    subprocess.run([sys.executable, agent_path])
                else:
                    # Get command from user
                    cmd = input(f"{GREEN}{agent_name}> {RESET}").strip()
                    if cmd.lower() != 'back':
                        run_agent(agent_path, cmd.split())
                
                input("\nPress Enter to continue...")
            else:
                print(f"{RED}Invalid choice{RESET}")
                input("Press Enter...")
        else:
            print(f"{RED}Invalid choice{RESET}")
            input("Press Enter...")

if __name__ == "__main__":
    main()