"""Enhanced LLM command with multi-provider fallback"""
import json
import requests
import os
import time
from pathlib import Path

from shared.llm.router import route

MODELS_DIR = Path("C:/Users/greg/dev/clawpack_v2/models")

def run(prompt, task_type=None):
    """Try multiple providers in priority order with intelligent routing."""
    # Detect task type from prompt if not specified
    if not task_type:
        if any(kw in prompt.lower() for kw in ["code", "function", "script", "program", "write a"]):
            task_type = "code_generation"
        elif any(kw in prompt.lower() for kw in ["plan", "orchestrate", "design", "architect"]):
            task_type = "planning"
    
    # Get routed provider
    preferred = route(task_type=task_type)
    if preferred:
        print(f"[llmclaw] Router selected: {preferred} for task_type={task_type}")
    config_path = MODELS_DIR / "active_model.json"
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except:
        return "Error: Could not load provider config"
    providers = config.get("providers", {})
    sorted_providers = sorted(providers.items(), key=lambda x: x[1].get("priority", 99))
        # If router specified a provider, prioritize it
    if preferred and preferred in providers:
        provider_config = providers[preferred]
        model = provider_config.get("model")
        timeout = provider_config.get("timeout", 30)
        print(f"[llmclaw] Trying routed {preferred}: {model}...")
        result = None
        if preferred == "direct_model": result = _ask_direct(prompt, model, timeout)
        elif preferred == "groq": result = _ask_groq(prompt, model, timeout)
        elif preferred == "ollama": result = _ask_ollama(prompt, model, timeout)
        elif preferred == "openrouter": result = _ask_openrouter(prompt, model, timeout)
        elif preferred == "anthropic": result = _ask_anthropic(prompt, model, timeout)
        if result and not result.startswith("Error"):
            return result
    
    for name, provider_config in sorted_providers:
        model = provider_config.get("model")
        timeout = provider_config.get("timeout", 30)
        print(f"[llmclaw] Trying {name}: {model}...")
        try:
            if name == "groq": result = _ask_groq(prompt, model, timeout)
            elif name == "ollama": result = _ask_ollama(prompt, model, timeout)
            elif name == "direct_model": result = _ask_direct(prompt, model, timeout)
            elif name == "openrouter": result = _ask_openrouter(prompt, model, timeout)
            elif name == "anthropic": result = _ask_anthropic(prompt, model, timeout)
            else: continue
            if result and not result.startswith("Error"):
                print(f"[llmclaw] Success with {name}")
                return result
            else:
                print(f"[llmclaw] {name} failed, trying next...")
        except Exception as e:
            print(f"[llmclaw] {name} error: {str(e)[:50]}")
            continue
    return "Error: All providers failed"

def _ask_direct(prompt, model, timeout):
    """Use direct model provider for obliterated models."""
    try:
        from shared.llm.providers.direct_model import generate
        return generate(prompt, model, max_tokens=128)
    except Exception as e:
        print(f"[llmclaw] Direct model error: {e}")
        return None

def _ask_ollama(prompt, model, timeout):
    response = requests.post("http://localhost:11434/api/generate", json={"model": model, "prompt": prompt, "stream": False}, timeout=timeout)
    if response.status_code == 200: return response.json().get("response", "")
    return None

def _ask_groq(prompt, model, timeout):
    api_key = _load_key("GROQ_API_KEY")
    if not api_key: return None
    for attempt in range(3):
        try:
            response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers={"Authorization": f"Bearer {api_key}"}, json={"model": model, "messages": [{"role": "user", "content": prompt}]}, timeout=timeout)
            if response.status_code == 200: return response.json()["choices"][0]["message"]["content"]
        except: pass
    return None

def _ask_openrouter(prompt, model, timeout):
    api_key = _load_key("OPENROUTER_API_KEY")
    if not api_key: return None
    for attempt in range(2):
        try:
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers={"Authorization": f"Bearer {api_key}"}, json={"model": model, "messages": [{"role": "user", "content": prompt}]}, timeout=timeout)
            if response.status_code == 200: return response.json()["choices"][0]["message"]["content"]
        except: pass
    return None

def _ask_anthropic(prompt, model, timeout):
    api_key = _load_key("ANTHROPIC_API_KEY")
    if not api_key: return None
    for attempt in range(3):
        try:
            response = requests.post("https://api.anthropic.com/v1/messages", headers={"x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"}, json={"model": model, "max_tokens": 4096, "messages": [{"role": "user", "content": prompt}]}, timeout=timeout)
            if response.status_code == 200: return response.json()["content"][0]["text"]
            elif response.status_code == 429: time.sleep(2 ** attempt)
        except: pass
    return None

def _load_key(key_name):
    env_path = Path("C:/Users/greg/dev/clawpack_v2/.env")
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith(f"{key_name}="): return line.split("=", 1)[1].strip()
    return os.environ.get(key_name)
