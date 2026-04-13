"""Obliterated models provider"""
import os
import sys
from pathlib import Path

# Add project root to path for sync import
PROJECT_ROOT = Path(r"C:\Users\greg\dev\clawpack_v2")
sys.path.insert(0, str(PROJECT_ROOT))

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

OBLITERATED_PATH = PROJECT_ROOT / "models" / "obliterated"

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_obliterated_models():
    models = []
    if not OBLITERATED_PATH.exists():
        return models
    for model_dir in OBLITERATED_PATH.iterdir():
        if model_dir.is_dir():
            config = model_dir / "config.json"
            if config.exists():
                size = sum(f.stat().st_size for f in model_dir.rglob('*') if f.is_file()) / (1024**3)
                metadata = model_dir / "abliteration_metadata.json"
                models.append({
                    'name': model_dir.name,
                    'path': str(model_dir),
                    'size_gb': size,
                    'is_obliterated': metadata.exists()
                })
    return sorted(models, key=lambda x: x['name'])

def sync_to_global_state(model_name, source):
    """Sync selected model to clawpack's global state"""
    try:
        # Update core state
        from core.state import STATE
        STATE.model = model_name
        STATE.provider = "obliterated"
        print(f"\n{GREEN}✅ Global state updated: {model_name}{RESET}")
    except Exception as e:
        print(f"\n{YELLOW}⚠️ Could not update global state: {e}{RESET}")
    
    try:
        # Update working_llms.json
        import json
        working_llms_path = PROJECT_ROOT / "working_llms.json"
        
        current = []
        if working_llms_path.exists():
            with open(working_llms_path, 'r') as f:
                current = json.load(f)
        
        # Add obliterated model with highest priority
        new_entry = {"model": model_name, "source": "local", "priority": 1, "obliterated": True}
        
        # Remove if exists, then insert at front
        current = [e for e in current if e.get("model") != model_name]
        current.insert(0, new_entry)
        
        with open(working_llms_path, 'w') as f:
            json.dump(current, f, indent=2)
        
        print(f"{GREEN}✅ working_llms.json updated{RESET}")
    except Exception as e:
        print(f"{YELLOW}⚠️ Could not update working_llms.json: {e}{RESET}")

def select_obliterated_model():
    from agents.llmclaw.core.state import set_active_model
    from agents.llmclaw.cli.interface import clear, banner
    
    models = get_obliterated_models()
    
    clear()
    banner()
    print(f"\n{GREEN}🔓 OBLITERATED MODELS{RESET}\n")
    
    if not models:
        print(f"{RED}❌ No obliterated models found!{RESET}")
        print(f"\n  {GREEN}[m]{RESET} 🏠 Return to Main Menu")
        input("\nPress Enter...")
        return
    
    for i, m in enumerate(models, 1):
        status = "🔓" if m['is_obliterated'] else "📦"
        print(f"  {GREEN}[{i}]{RESET} {status} {m['name']} ({m['size_gb']:.2f} GB)")
    
    print(f"\n  {GREEN}[m]{RESET} 🏠 Return to Main Menu")
    
    choice = input(f"\n{BOLD}{YELLOW}Select model or 'm' for menu: {RESET}").strip()
    
    if choice.lower() == 'm':
        return
    
    if choice.isdigit() and 1 <= int(choice) <= len(models):
        selected = models[int(choice) - 1]
        set_active_model(selected['name'], 'obliterated')
        
        # SYNC TO GLOBAL STATE
        sync_to_global_state(selected['name'], 'obliterated')
        
        print(f"\n{GREEN}✅ Activated: {selected['name']}{RESET}")
        input("Press Enter...")
