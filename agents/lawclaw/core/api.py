"""API - AI and web requests"""

import urllib.request
import json
import subprocess
from .config import get_api_key

def ask_ai(question):
    api_key = get_api_key()
    if api_key:
        return _ask_openrouter(question, api_key)
    return _ask_ollama(question)

def _ask_openrouter(question, api_key):
    data = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a judicial research assistant. Provide accurate legal information."},
            {"role": "user", "content": question}
        ]
    }
    try:
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps(data).encode('utf-8'),
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())['choices'][0]['message']['content']
    except Exception as e:
        return f"API Error: {e}"

def _ask_ollama(question):
    try:
        result = subprocess.run(['ollama', 'run', 'deepseek-coder:6.7b', question],
                                capture_output=True, text=True, timeout=60)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"Error: {e}"

def fetch_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'LawClaw/1.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            import re
            text = re.sub(r'<[^>]+>', ' ', content)
            text = re.sub(r'\s+', ' ', text)
            return text
    except Exception as e:
        return f"Error: {e}"
