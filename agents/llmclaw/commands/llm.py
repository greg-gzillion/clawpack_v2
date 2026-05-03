"""Enhanced LLM command with multi-provider fallback"""
import json
import requests
import os
import time
from pathlib import Path

from shared.llm.router import route
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent


MODELS_DIR = PROJECT_ROOT / "models"

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
    # Override: code tasks always use cloud models, not obliterated
    if preferred == "direct_model" and task_type in ("code_generation", "code_drafting"):
        preferred = "anthropic"
        print(f"[llmclaw] Override: code task -> anthropic instead of direct_model")
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

def run(prompt, task_type=None):
    """Constitutional: ALL model access routes through shared/llm/client.py"""
    import asyncio
    from shared.llm.config import load_config
    from shared.llm.client import get_llm_client
    
    if not task_type:
        if any(kw in prompt.lower() for kw in ["code", "function", "script", "program", "write a"]):
            task_type = "code_generation"
    
    config = load_config()
    model = config.get("model", "anthropic")
    provider = config.get("source", "groq")
    
    print(f"[llmclaw] Sovereign Gateway: {provider}/{model}")
    try:
        client = get_llm_client()
        result = asyncio.run(client.call(
            prompt=prompt, agent='llmclaw', model=model,
            provider=provider, max_tokens=4096, temperature=0.7
        ))
        return result.content if result else "Error: No response from Gateway"
    except Exception as e:
        print(f"[llmclaw] Gateway error: {e}")
        return f"Error: {str(e)[:200]}"
