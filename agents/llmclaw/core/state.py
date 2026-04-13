"""Model state management - with global sync"""

import json
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\greg\dev\clawpack_v2")
STATE_FILE = PROJECT_ROOT / "models" / "active_model.json"

def get_active_model():
    try:
        if STATE_FILE.exists():
            with open(STATE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('model'), data.get('source')
    except:
        pass
    return None, None

def set_active_model(model, source):
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump({'model': model, 'source': source}, f)
        
        # Sync to global state
        try:
            from agents.llmclaw.core.sync import sync_model_to_global_state
            sync_model_to_global_state()
        except:
            pass
        
        return True
    except:
        return False

def get_model_paths():
    return {
        'obliterated': PROJECT_ROOT / "models" / "obliterated",
        'stock': PROJECT_ROOT / "models" / "stock",
    }
