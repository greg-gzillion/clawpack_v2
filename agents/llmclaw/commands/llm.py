"""Enhanced LLM command with multi-provider fallback"""
import json
import requests
import os
import time
from pathlib import Path

MODELS_DIR = Path("C:/Users/greg/dev/clawpack_v2/models")

def run(prompt):
    """Route through sovereign gateway — the ONLY legal path to model access."""
    try:
        from shared.llm import get_llm_client
        client = get_llm_client()
        response = client.call_sync(prompt=prompt, agent="llmclaw")
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"

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
