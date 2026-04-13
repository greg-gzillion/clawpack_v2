"""LLMClaw Integration - Updates global state with selected model"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
STATE_FILE = PROJECT_ROOT / "models" / "active_model.json"
WORKING_LLMS_FILE = PROJECT_ROOT / "working_llms.json"

def sync_model_to_global_state():
    """Sync LLMClaw's selected model to clawpack's global state"""
    
    if not STATE_FILE.exists():
        return None
    
    try:
        with open(STATE_FILE, 'r') as f:
            data = json.load(f)
            model = data.get('model')
            source = data.get('source')
            
        if not model:
            return None
        
        # Update core/state.py's STATE
        try:
            from core.state import STATE
            STATE.model = model
            STATE.provider = source if source == "stock" else "obliterated"
            print(f"✅ Global state updated: {model}")
        except ImportError:
            pass
        
        # Update working_llms.json
        update_working_llms(model, source)
        
        return model, source
        
    except Exception as e:
        print(f"Error syncing model: {e}")
        return None

def update_working_llms(model: str, source: str):
    """Add selected model to working_llms.json with priority"""
    
    current_llms = []
    if WORKING_LLMS_FILE.exists():
        with open(WORKING_LLMS_FILE, 'r') as f:
            current_llms = json.load(f)
    
    # Determine source type
    source_type = "ollama" if source == "stock" else "local"
    
    # Check if model already exists
    existing = None
    for item in current_llms:
        if item.get("model") == model:
            existing = item
            break
    
    if existing:
        # Move to front
        current_llms.remove(existing)
        current_llms.insert(0, existing)
    else:
        # Add new entry
        current_llms.insert(0, {
            "model": model,
            "source": source_type,
            "priority": 1 if source == "obliterated" else 2
        })
    
    # Keep only top 10
    current_llms = current_llms[:10]
    
    with open(WORKING_LLMS_FILE, 'w') as f:
        json.dump(current_llms, f, indent=2)
    
    print(f"✅ working_llms.json updated")

if __name__ == "__main__":
    result = sync_model_to_global_state()
    if result:
        print(f"Active: {result[0]} ({result[1]})")
