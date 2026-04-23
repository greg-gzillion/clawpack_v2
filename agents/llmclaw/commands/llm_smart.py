"""Smart LLM Router - Chooses obliterated vs normal based on task"""
import json
from pathlib import Path

MODELS_DIR = Path("C:/Users/greg/dev/clawpack_v2/models")

# Keywords that suggest we should use obliterated models
OBLITERATED_KEYWORDS = [
    "hack", "exploit", "vulnerability", "pentest", "password", "crack",
    "bypass", "security test", "red team", "keylogger", "malware",
    "unrestricted", "no limits", "without restrictions"
]

def should_use_obliterated(prompt: str) -> bool:
    """Determine if task needs an obliterated model"""
    prompt_lower = prompt.lower()
    for keyword in OBLITERATED_KEYWORDS:
        if keyword in prompt_lower:
            return True
    return False

def run(prompt: str) -> str:
    """Route to appropriate model based on task"""
    
    # Load config
    config_path = MODELS_DIR / "active_model.json"
    with open(config_path) as f:
        config = json.load(f)
    
    # Check if we should use obliterated
    if should_use_obliterated(prompt):
        print("[llmclaw] Using OBLITERATED model (no refusals)")
        
        # Try obliterated models first
        obliterated_models = config.get("obliterated_models", [])
        for model in obliterated_models:
            try:
                from commands.llm_enhanced import _ask_ollama
                result = _ask_ollama(prompt, model, 60)
                if result:
                    return result
            except:
                continue
        
        # Fallback to normal providers
        print("[llmclaw] Obliterated failed, falling back...")
    
    # Normal routing - use enhanced multi-provider
    print("[llmclaw] Using standard multi-provider")
    from commands.llm_enhanced import run as enhanced_run
    return enhanced_run(prompt)
