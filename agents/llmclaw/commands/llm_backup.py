"""LLM command - Multi-provider LLM interface"""
import requests
import json
import os
from pathlib import Path

name = "/llm"
MODELS_DIR = Path("str(PROJECT_ROOT)/models")

def run(prompt):
    if not prompt:
        return "Usage: /llm <prompt>"
    
    try:
        prompt = str(prompt).strip()[:2000]
        
        with open(MODELS_DIR / "active_model.json", 'r') as f:
            active = json.load(f)
        model = active.get("model", "gemma3:12b")
        source = active.get("source", "stock")
        
        print(f"[llmclaw] Using {model} ({source})")
        
        # Route to provider
        if source in ["stock", "ollama"]:
            return _ask_ollama(prompt, model)
        elif source == "groq":
            return _ask_groq(prompt, model)
        elif source == "openrouter":
            return _ask_openrouter(prompt, model)
        else:
            return f"Unknown source: {source}"
            
    except Exception as e:
        return f"LLM error: {str(e)[:200]}"

def _ask_ollama(prompt, model):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=60
    )
    if response.status_code == 200:
        return response.json()["response"]
    return f"Ollama error: {response.status_code}"

def _ask_groq(prompt, model):
    api_key = _load_key("GROQ_API_KEY")
    if not api_key:
        return "Error: GROQ_API_KEY not found"
    
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7},
        timeout=60
    )
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    return f"Groq error: {response.status_code}"

def _ask_openrouter(prompt, model):
    api_key = _load_key("OPENROUTER_API_KEY")
    if not api_key:
        return "Error: OPENROUTER_API_KEY not found"
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model, "messages": [{"role": "user", "content": prompt}]},
        timeout=60
    )
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    return f"OpenRouter error: {response.status_code}"

def _load_key(key_name):
    env_path = Path("str(PROJECT_ROOT)/.env")
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith(f"{key_name}="):
                    return line.split("=", 1)[1].strip()
    return os.environ.get(key_name)
