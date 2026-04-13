"""LLMClaw interactive menu interface"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print(f"""{CYAN}
╔══════════════════════════════════════════════════════════════╗
║                    🦞 LLMCLAW - MODEL MANAGER                 ║
╚══════════════════════════════════════════════════════════════╝{RESET}
""")

def main_menu():
    """Main LLMClaw menu"""
    from agents.llmclaw.core.state import get_active_model, set_active_model
    
    while True:
        clear()
        banner()
        
        model, source = get_active_model()
        if model:
            source_display = "🔓 Obliterated" if source == "obliterated" else "📦 Stock"
            print(f"{CYAN}Active: {GREEN}{model}{CYAN} ({source_display}){RESET}\n")
        
        print(f"{YELLOW}Select Model Source:{RESET}\n")
        print(f"  {GREEN}[1]{RESET} 📦 Stock Models (Ollama)")
        print(f"  {GREEN}[2]{RESET} 🔓 Obliterated Models")
        print(f"  {GREEN}[3]{RESET} ☁️  API Providers")
        print(f"  {GREEN}[4]{RESET} 🤖 Proceed to Agent Selection")
        print(f"  {GREEN}[5]{RESET} 🏠 Exit")
        
        choice = input(f"\n{BOLD}{YELLOW}📋 Select: {RESET}").strip()
        
        if choice == '1':
            from agents.llmclaw.providers.stock import select_stock_model
            select_stock_model()
        elif choice == '2':
            from agents.llmclaw.providers.obliterated import select_obliterated_model
            select_obliterated_model()
        elif choice == '3':
            print(f"\n{YELLOW}☁️ API providers coming soon!{RESET}")
            input("Press Enter...")
        elif choice == '4':
    # LAUNCH AGENT MENU
        clear()
        print(f"{GREEN}🦞 Launching Clawpack Agent Selection...{RESET}\n")
        import subprocess
        import sys
    # Use the dedicated menu script that stays open
        subprocess.run([sys.executable, "agents_menu.py"])
    # Return to LLMClaw menu after agents_menu exits
        elif choice == '5':
            clear()
            print(f"{GREEN}👋 Goodbye!{RESET}")
            break

if __name__ == "__main__":
    result = main_menu()
    if result == "proceed_to_agents":
        print("PROCEED_TO_AGENTS")
    elif result == "main_menu":
        print("MAIN_MENU")
