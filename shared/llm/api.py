"""Shared LLM API Module - For ALL Clawpack Agents"""

import os
import requests
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
ENV_PATH = ROOT_DIR / ".env"

API_KEY = None

if ENV_PATH.exists():
    with open(ENV_PATH, 'r', encoding='utf-8-sig') as f:  # utf-8-sig removes BOM automatically
        for line in f:
            line = line.strip()
            if 'OPENROUTER_API_KEY' in line and '=' in line:
                key_part = line.split('=', 1)[1].strip()
                key_part = key_part.strip('"\'').strip()
                if key_part and len(key_part) > 20:
                    API_KEY = key_part
                    break

def call(prompt: str, model: str = "openai/gpt-3.5-turbo", max_tokens: int = 2000) -> str:
    if not API_KEY:
        return "ERROR: OPENROUTER_API_KEY not found in .env"
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json={"model": model, "messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens},
            timeout=60
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return f"API Error ({response.status_code})"
    except Exception as e:
        return f"Error: {e}"

def test() -> bool:
    result = call("Say OK", max_tokens=5)
    return "OK" in result and "ERROR" not in result

def get_status() -> dict:
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
