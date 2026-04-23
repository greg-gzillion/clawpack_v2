#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         🦞 CLAWPACK V2 - AI AGENT ECOSYSTEM                    ║
║                         Modular | AI-Powered | 19 Specialized Agents          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

# ============================================================================
# COLORS - Make it look GREAT
# ============================================================================
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
BOLD = '\033[1m'
RESET = '\033[0m'

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print(f"""{CYAN}
╔══════════════════════════════════════════════════════════════════════════════╗
║                         🦞 {BOLD}CLAWPACK V2 - AI AGENT ECOSYSTEM{RESET}{CYAN}                        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  {GREEN}🤖 19 AI Agents  │  🧠 LLM Powered  │  🔗 A2A Ready  │  📚 Chronicle{RESET}{CYAN}        ║
╚══════════════════════════════════════════════════════════════════════════════╝{RESET}
""")

# ============================================================================
# AGENT REGISTRY - Complete with ALL your agents
# ============================================================================
AGENTS = [
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
    {"num": 14, "name": "medicclaw",       "emoji": "🏥",  "desc": "Medical References"},
    {"num": 15, "name": "dreamclaw",       "emoji": "🎨",  "desc": "AI Vision & Generation"},
    {"num": 16, "name": "designclaw",      "emoji": "🎯",  "desc": "Graphic Design"},
    {"num": 17, "name": "draftclaw",       "emoji": "📏",  "desc": "Technical Drawings"},
    {"num": 18, "name": "crustyclaw",      "emoji": "🦀",  "desc": "Rust AI Assistant"},
    {"num": 19, "name": "rustypycraw",     "emoji": "🔍",  "desc": "Code Crawler"},
]

def show_agents():
    print(f"{BOLD}{CYAN}┌────────────────────────────────────────────────────────────────────────┐{RESET}")
    print(f"{BOLD}{CYAN}│                         🤖 AVAILABLE AGENTS                             │{RESET}")
    print(f"{BOLD}{CYAN}├────────────────────────────────────────────────────────────────────────┤{RESET}")
    for a in AGENTS:
        print(f"{CYAN}│  {GREEN}{a['num']:2}{RESET}  {a['emoji']}  {BOLD}{a['name']:16}{RESET}  {YELLOW}{a['desc']}{RESET}")
    print(f"{BOLD}{CYAN}├────────────────────────────────────────────────────────────────────────┤{RESET}")
    print(f"{CYAN}│  {GREEN}q{RESET}  🚪  {RED}Quit{RESET}                                                          {CYAN}│{RESET}")
    print(f"{BOLD}{CYAN}└────────────────────────────────────────────────────────────────────────┘{RESET}")

# ============================================================================
# AGENT MENU SYSTEM - Each agent shows its commands
# ============================================================================
AGENT_COMMANDS = {
    "lawclaw": """
╔════════════════════════════════════════════════════════════════════════════╗
║  ⚖️ LAWCLAW - AI Law Research Assistant                                  ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║  COMMANDS:                                                                  ║
║    /ask <question>        - Ask any law question (AI answers)            ║
║    /search <topic>        - Research law topic (AI analyzes)             ║
║    /court <ST> <county>   - Display local court info                       ║
║                                                                             ║
║  EXAMPLES:                                                                  ║
║    /ask What is the statute of limitations for contract breach?            ║
║    /search fourth amendment                                                ║
║    /court CO Clear Creek                                                   ║
║                                                                             ║
╚════════════════════════════════════════════════════════════════════════════╝""",
    
    "flowclaw": """
╔════════════════════════════════════════════════════════════════════════════╗
║  📊 FLOWCLAW - AI Diagram Generator                                        ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║  COMMANDS:                                                                  ║
║    /flowchart <desc>     - Generate flowchart                             ║
║    /sequence <desc>      - Generate sequence diagram                      ║
║    /architecture <desc>  - Generate architecture diagram                  ║
║    /gantt <desc>         - Generate Gantt chart                           ║
║                                                                             ║
║  EXAMPLES:                                                                  ║
║    /flowchart user login process                                           ║
║    /sequence API call flow                                                 ║
║                                                                             ║
╚════════════════════════════════════════════════════════════════════════════╝""",

    "mathematicaclaw": """
╔════════════════════════════════════════════════════════════════════════════╗
║  📐 MATHEMATICACLAW - AI Math Visualization                                ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║  COMMANDS:                                                                  ║
║    /visualize <desc>     - AI-powered math visualization                  ║
║    /solve <equation>     - Solve mathematical equation                    ║
║    /plot <function>      - Plot function graph                            ║
║                                                                             ║
║  EXAMPLES:                                                                  ║
║    /visualize 3D mountain                                                 ║
║    /solve x^2 + 2x - 8 = 0                                                ║
║                                                                             ║
╚════════════════════════════════════════════════════════════════════════════╝""",

    "liberateclaw": """
╔════════════════════════════════════════════════════════════════════════════╗
║  🔓 LIBERATECLAW - LLM Model Liberation                                    ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║  COMMANDS:                                                                  ║
║    /models              - List available models                           ║
║    /liberate <model>    - Download/liberate a model                       ║
║    /use <model> <prompt> - Run inference with model                       ║
║    /liberated           - List liberated models                           ║
║                                                                             ║
║  EXAMPLES:                                                                  ║
║    /liberate llama3.2:3b                                                  ║
║    /use llama3.2:3b "Explain blockchain"                                  ║
║                                                                             ║
╚════════════════════════════════════════════════════════════════════════════╝""",
}

def get_agent_commands(agent_name):
    if agent_name in AGENT_COMMANDS:
        return AGENT_COMMANDS[agent_name]
    return f"""
╔════════════════════════════════════════════════════════════════════════════╗
║  🦞 {agent_name.upper()} - AI Agent                                         ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║  Type 'back' to return to main menu                                        ║
║  Type 'help' to see this help                                             ║
║                                                                             ║
╚════════════════════════════════════════════════════════════════════════════╝"""

# ============================================================================
# MAIN MENU
# ============================================================================
def run_agent(agent_name):
    agent_path = PROJECT_ROOT / "agents" / agent_name / f"{agent_name}.py"
    
    if not agent_path.exists():
        print(f"{RED}❌ Agent {agent_name} not found{RESET}")
        input("Press Enter to continue...")
        return
    
    clear()
    print(get_agent_commands(agent_name))
    print(f"\n{YELLOW}💡 Type 'back' to return to main menu{RESET}\n")
    
    while True:
        try:
            cmd = input(f"{GREEN}{agent_name}> {RESET}").strip()
            
            if cmd.lower() == 'back':
                break
            elif cmd.lower() == 'help':
                clear()
                print(get_agent_commands(agent_name))
                print(f"\n{YELLOW}💡 Type 'back' to return to main menu{RESET}\n")
                continue
            elif cmd:
                # Run the agent with the command
                result = subprocess.run(
                    [sys.executable, str(agent_path)] + cmd.split(),
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                print(result.stdout if result.stdout else result.stderr)
                print()
        except KeyboardInterrupt:
            break
        except subprocess.TimeoutExpired:
            print(f"{RED}❌ Command timed out{RESET}\n")
        except Exception as e:
            print(f"{RED}❌ Error: {e}{RESET}\n")

# ============================================================================
# MAIN
# ============================================================================
def main():
    while True:
        clear()
        banner()
        show_agents()
        
        choice = input(f"\n{BOLD}{YELLOW}📋 Select agent (1-19) or 'q' to quit: {RESET}").strip()
        
        if choice.lower() == 'q':
            clear()
            print(f"{GREEN}🦞 Goodbye!{RESET}\n")
            break
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(AGENTS):
                run_agent(AGENTS[idx]["name"])
            else:
                print(f"{RED}❌ Invalid choice{RESET}")
                input("Press Enter...")
        else:
            print(f"{RED}❌ Invalid choice{RESET}")
            input("Press Enter...")

if __name__ == "__main__":
    main()
