"""Stock models provider (Ollama)"""
import os
import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\greg\dev\clawpack_v2")
sys.path.insert(0, str(PROJECT_ROOT))

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_stock_models():
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        models = []
        lines = result.stdout.strip().split('\n')[1:]
        for line in lines:
            if line.strip():
                parts = line.split()
                if parts:
                    models.append({'name': parts[0], 'source': 'stock'})
        return models
    except:
        return []

def sync_to_global_state(model_name, source):
    """Sync selected model to clawpack's global state"""
    try:
        from core.state import STATE
        STATE.model = model_name
        STATE.provider = "ollama"
        print(f"\n{GREEN}✅ Global state updated: {model_name}{RESET}")
    except Exception as e:
        print(f"\n{YELLOW}⚠️ Could not update global state: {e}{RESET}")
    
    try:
        import json
        working_llms_path = PROJECT_ROOT / "working_llms.json"
        
        current = []
        if working_llms_path.exists():
            with open(working_llms_path, 'r') as f:
                current = json.load(f)
        
        new_entry = {"model": model_name, "source": "ollama", "priority": 2}
        
        current = [e for e in current if e.get("model") != model_name]
        current.insert(0, new_entry)
        
        with open(working_llms_path, 'w') as f:
            json.dump(current, f, indent=2)
        
        print(f"{GREEN}✅ working_llms.json updated{RESET}")
    except Exception as e:
        print(f"{YELLOW}⚠️ Could not update working_llms.json: {e}{RESET}")

def select_stock_model():
    from agents.llmclaw.core.state import set_active_model
    from agents.llmclaw.cli.interface import clear, banner
    
    models = get_stock_models()
    
    clear()
    banner()
    print(f"\n{GREEN}📦 STOCK MODELS (OLLAMA){RESET}\n")
    
    if not models:
        print(f"{RED}❌ No Ollama models found!{RESET}")
        print(f"\n  {GREEN}[m]{RESET} 🏠 Return to Main Menu")
        input("\nPress Enter...")
        return
    
    for i, m in enumerate(models, 1):
        print(f"  {GREEN}[{i}]{RESET} 📦 {m['name']}")
    
    print(f"\n  {GREEN}[m]{RESET} 🏠 Return to Main Menu")
    
    choice = input(f"\n{BOLD}{YELLOW}Select model or 'm' for menu: {RESET}").strip()
    
    if choice.lower() == 'm':
        return
    
    if choice.isdigit() and 1 <= int(choice) <= len(models):
        selected = models[int(choice) - 1]
        set_active_model(selected['name'], 'stock')
        
        # SYNC TO GLOBAL STATE
        sync_to_global_state(selected['name'], 'stock')
        
        print(f"\n{GREEN}✅ Activated: {selected['name']}{RESET}")
        input("Press Enter...")
