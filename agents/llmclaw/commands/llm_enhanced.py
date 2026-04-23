"""Enhanced LLM command with multi-provider fallback"""
import json
import requests
import os
from pathlib import Path

MODELS_DIR = Path("C:/Users/greg/dev/clawpack_v2/models")

def run(prompt):
    """Try multiple providers in priority order"""
    config_path = MODELS_DIR / "active_model.json"
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except:
        return "Error: Could not load provider config"
    
    # Get providers in priority order
    providers = config.get("providers", {})
    sorted_providers = sorted(providers.items(), key=lambda x: x[1].get("priority", 99))
    
    for name, provider_config in sorted_providers:
        model = provider_config.get("model")
        timeout = provider_config.get("timeout", 30)
        
        print(f"[llmclaw] Trying {name}: {model}...")
        
        try:
            if name == "groq":
                result = _ask_groq(prompt, model, timeout)
            elif name == "ollama":
                result = _ask_ollama(prompt, model, timeout)
            elif name == "openrouter":
                result = _ask_openrouter(prompt, model, timeout)
            elif name == "anthropic":
                result = _ask_anthropic(prompt, model, timeout)
            else:
                continue
            
            if result and not result.startswith("Error"):
                print(f"[llmclaw] Success with {name}")
                return result
            else:
                print(f"[llmclaw] {name} failed, trying next...")
                
        except Exception as e:
            print(f"[llmclaw] {name} error: {str(e)[:50]}")
            continue
    
    return "Error: All providers failed"

def _ask_ollama(prompt, model, timeout):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=timeout
    )
    if response.status_code == 200:
        return response.json().get("response", "")
    return None

def _ask_groq(prompt, model, timeout):
    api_key = _load_key("GROQ_API_KEY")
    if not api_key:
        return None
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": model, "messages": [{"role": "user", "content": prompt}]},
        timeout=timeout
    )
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    return None

def _ask_openrouter(prompt, model, timeout):
    api_key = _load_key("OPENROUTER_API_KEY")
    if not api_key:
        return None
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": model, "messages": [{"role": "user", "content": prompt}]},
        timeout=timeout
    )
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    return None

def _ask_anthropic(prompt, model, timeout):
    # Simplified - would need SDK
    return None

def _load_key(key_name):
    env_path = Path("C:/Users/greg/dev/clawpack_v2/.env")
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith(f"{key_name}="):
                    return line.split("=", 1)[1].strip()
    return os.environ.get(key_name)
