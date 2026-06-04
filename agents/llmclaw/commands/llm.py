"""LLM command - Multi-provider with fallback, obliterated support, and intelligent routing"""
import json
import requests
import os
import asyncio
from pathlib import Path

name = "/llm"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
MODELS_DIR = PROJECT_ROOT / "models"

# Keywords for obliterated model routing
OBLITERATED_KEYWORDS = [
    "hack", "exploit", "vulnerability", "pentest", "password", "crack",
    "bypass", "security test", "red team", "keylogger", "malware",
    "unrestricted", "no limits", "without restrictions"
]


def should_use_obliterated(prompt):
    prompt_lower = prompt.lower()
    for keyword in OBLITERATED_KEYWORDS:
        if keyword in prompt_lower:
            return True
    return False


def run(prompt, task_type=None):
    """Try multiple providers in priority order with intelligent routing."""
    if not prompt:
        return "Usage: /llm <prompt>"

    prompt = str(prompt).strip()[:2000]

    # Detect task type from prompt if not specified
    if not task_type:
        if any(kw in prompt.lower() for kw in ["code", "function", "script", "program", "write a"]):
            task_type = "code_generation"
        elif any(kw in prompt.lower() for kw in ["plan", "orchestrate", "design", "architect"]):
            task_type = "planning"

    # Check for obliterated routing
    if should_use_obliterated(prompt):
        print("[llmclaw] Routing to obliterated model (no refusals)")
        obliterated_dir = MODELS_DIR / "obliterated"
        if obliterated_dir.exists():
            for d in sorted(obliterated_dir.iterdir()):
                if d.is_dir() and (d / "config.json").exists():
                    try:
                        from shared.llm.providers.direct_model import generate
                        result = generate(prompt, d.name, max_tokens=512)
                        if result:
                            return result
                    except:
                        continue
        print("[llmclaw] Obliterated failed, falling back to standard providers")

    # Load config
    try:
        with open(MODELS_DIR / "active_model.json") as f:
            config = json.load(f)
    except:
        return "Error: Could not load provider config"

    providers = config.get("providers", {})

    # Intelligent routing via shared/llm/router.py
    try:
        from shared.llm.router import route
        preferred = route(task_type=task_type)
    except:
        preferred = None

    if preferred:
        print(f"[llmclaw] Router selected: {preferred} for task_type={task_type}")

    # Override: code tasks always use cloud models, not obliterated
    if preferred == "direct_model" and task_type in ("code_generation", "code_drafting"):
        preferred = "anthropic"
        print(f"[llmclaw] Override: code task -> anthropic instead of direct_model")

    # Try preferred provider first
    if preferred and preferred in providers:
        provider_config = providers[preferred]
        model = provider_config.get("model")
        timeout = provider_config.get("timeout", 30)
        print(f"[llmclaw] Trying routed {preferred}: {model}...")
        result = _call_provider(preferred, prompt, model, timeout)
        if result and not result.startswith("Error"):
            return result

    # Full fallback chain
    sorted_providers = sorted(providers.items(), key=lambda x: x[1].get("priority", 99))
    for name, provider_config in sorted_providers:
        model = provider_config.get("model")
        timeout = provider_config.get("timeout", 30)
        print(f"[llmclaw] Trying {name}: {model}...")
        try:
            result = _call_provider(name, prompt, model, timeout)
            if result and not result.startswith("Error"):
                print(f"[llmclaw] Success with {name}")
                return result
            else:
                print(f"[llmclaw] {name} failed, trying next...")
        except Exception as e:
            print(f"[llmclaw] {name} error: {str(e)[:50]}")
            continue

    return "Error: All providers failed"


def _call_provider(name, prompt, model, timeout):
    """Route to the correct provider function."""
    if name == "direct_model":
        return _ask_direct(prompt, model, timeout)
    elif name == "groq":
        return _ask_groq(prompt, model, timeout)
    elif name in ("ollama", "obliterated"):
        return _ask_ollama(prompt, model, timeout)
    elif name == "openrouter":
        return _ask_openrouter(prompt, model, timeout)
    elif name == "anthropic":
        return _ask_anthropic(prompt, model, timeout)
    return None


def _ask_direct(prompt, model, timeout):
    """Use direct model provider for obliterated models."""
    try:
        from shared.llm.providers.direct_model import generate
        return generate(prompt, model, max_tokens=512)
    except Exception as e:
        print(f"[llmclaw] Direct model error: {e}")
        return None


def _ask_ollama(prompt, model, timeout):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False, "options": {"num_predict": 500}},
        timeout=timeout
    )
    if response.status_code == 200:
        return response.json().get("response", "")
    return None


def _ask_groq(prompt, model, timeout):
    api_key = _load_key("GROQ_API_KEY")
    if not api_key:
        return None
    for attempt in range(3):
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={"model": model, "messages": [{"role": "user", "content": prompt}]},
                timeout=timeout
            )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
        except:
            pass
    return None


def _ask_openrouter(prompt, model, timeout):
    api_key = _load_key("OPENROUTER_API_KEY")
    if not api_key:
        return None
    for attempt in range(2):
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={"model": model, "messages": [{"role": "user", "content": prompt}]},
                timeout=timeout
            )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
        except:
            pass
    return None


def _ask_anthropic(prompt, model, timeout):
    api_key = _load_key("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 2000
            },
            timeout=timeout
        )
        if response.status_code == 200:
            data = response.json()
            return data["content"][0]["text"].strip()
    except Exception as e:
        print(f"[llmclaw] Anthropic error: {e}")
    return None


def _load_key(key_name):
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith(f"{key_name}="):
                    return line.split("=", 1)[1].strip()
    return os.environ.get(key_name)