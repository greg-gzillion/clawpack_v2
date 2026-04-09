"""Shared LLM API Module - Fixed for OpenRouter"""

import os
import requests
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
ENV_PATH = ROOT_DIR / ".env"

# Working OpenRouter models
WORKING_MODELS = [
    "google/gemini-2.0-flash-lite-preview-02-05:free",
    "microsoft/phi-3-mini-128k-instruct:free",
    "meta-llama/llama-3.2-3b-instruct:free",
    "openrouter/auto"
]

def get_api_key():
    """Get API key from .env file"""
    if ENV_PATH.exists():
        try:
            with open(ENV_PATH, 'r', encoding='utf-8-sig') as f:
                for line in f:
                    line = line.strip()
                    if 'OPENROUTER_API_KEY' in line and '=' in line:
                        key = line.split('=', 1)[1].strip()
                        key = key.strip('"\'').strip()
                        if key and len(key) > 20:
                            return key
        except Exception as e:
            print(f"Error reading .env: {e}")
    return None

API_KEY = get_api_key()

def call(prompt: str, model: str = None, max_tokens: int = 1000) -> str:
    """Make a call to OpenRouter API"""
    if not API_KEY:
        return "ERROR: OPENROUTER_API_KEY not found in .env"
    
    # Use a working model
    if not model or model == "openai/gpt-3.5-turbo":
        model = WORKING_MODELS[0]  # Use Gemini Flash Lite (free)
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://clawpack.ai",
                "X-Title": "Clawpack Agent"
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.7
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            # Try fallback model
            if model != WORKING_MODELS[1]:
                return call(prompt, WORKING_MODELS[1], max_tokens)
            return f"API Error ({response.status_code}): {response.text[:200]}"
            
    except Exception as e:
        return f"Error: {e}"

def test() -> bool:
    """Test if API is working"""
    result = call("Say OK", max_tokens=5)
    return result and "OK" in result and "ERROR" not in result

def get_status() -> dict:
    """Get API status"""
    return {
        "key_loaded": bool(API_KEY),
        "key_preview": API_KEY[:20] + "..." if API_KEY else None,
        "env_path": str(ENV_PATH),
        "env_exists": ENV_PATH.exists(),
        "working": test()
    }

if __name__ == "__main__":
    print("=== Shared LLM API Module ===")
    print(f"ENV path: {ENV_PATH}")
    print(f"ENV exists: {ENV_PATH.exists()}")
    print(f"API Key: {API_KEY[:20] if API_KEY else 'NOT FOUND'}...")
    print(f"API test: {'✅ WORKING' if test() else '❌ FAILED'}")
