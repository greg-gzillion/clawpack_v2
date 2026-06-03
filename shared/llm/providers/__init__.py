"""Provider detection and routing."""
import requests
from typing import Dict, List
from ..response import LLMProvider

def check_ollama():
    try:
        r = requests.get('http://localhost:11434/api/tags', timeout=2)
        return r.status_code == 200
    except Exception:
        return False

def detect_providers(config):
    providers = []
    # Read priority settings from active_model.json
    _priorities = {}
    try:
        import json as _j
        _am = _j.loads(open('models/active_model.json').read())
        for _pname, _pdata in _am.get('providers', {}).items():
            _priorities[_pname] = _pdata.get('priority', 99)
    except Exception:
        pass
    # Build provider list
    if config.get('GROQ_API_KEY'):
        providers.append({'type': LLMProvider.GROQ, 'key': config['GROQ_API_KEY'], 'model': 'llama-3.3-70b-versatile', 'base_url': 'https://api.groq.com/openai/v1', 'cost_per_call': 0.0, 'priority': _priorities.get('groq', 1)})
    if check_ollama():
        try:
            import json as _j2
            am2 = _j2.loads(open('models/active_model.json').read())
            ollama_model = am2.get('model', 'deepseek-r1:8b')
        except Exception:
            ollama_model = 'deepseek-r1:8b'
        providers.append({'type': LLMProvider.OLLAMA, 'model': ollama_model, 'base_url': 'http://localhost:11434', 'cost_per_call': 0.0, 'priority': _priorities.get('ollama', 2)})
    if config.get('OPENROUTER_API_KEY'):
        providers.append({'type': LLMProvider.OPENROUTER, 'key': config['OPENROUTER_API_KEY'], 'model': 'google/gemma-4-26b-a4b-it:free', 'base_url': 'https://openrouter.ai/api/v1', 'cost_per_call': 0.002, 'priority': _priorities.get('openrouter', 3)})
    if config.get('ANTHROPIC_API_KEY'):
        providers.append({'type': LLMProvider.ANTHROPIC, 'key': config['ANTHROPIC_API_KEY'], 'model': 'claude-haiku-4-5-20251001', 'base_url': 'https://api.anthropic.com/v1', 'cost_per_call': 0.015, 'priority': _priorities.get('anthropic', 4)})
    if config.get('OPENAI_API_KEY'):
        providers.append({'type': LLMProvider.OPENAI, 'key': config['OPENAI_API_KEY'], 'model': 'gpt-4o', 'base_url': 'https://api.openai.com/v1', 'cost_per_call': 0.01, 'priority': _priorities.get('openai', 5)})
    # Sort by priority (lower number = higher priority)
    providers.sort(key=lambda p: p.get('priority', 99))
    return providers
