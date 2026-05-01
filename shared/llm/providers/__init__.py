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
    if check_ollama():
        providers.append({'type': LLMProvider.OLLAMA, 'model': 'qwen3-coder:30b', 'base_url': 'http://localhost:11434', 'cost_per_call': 0.0})
    if config.get('OPENROUTER_API_KEY'):
        providers.append({'type': LLMProvider.OPENROUTER, 'key': config['OPENROUTER_API_KEY'], 'model': config.get('OPENROUTER_MODEL', 'z-ai/glm-5.1'), 'base_url': 'https://openrouter.ai/api/v1', 'cost_per_call': 0.002})
    if config.get('ANTHROPIC_API_KEY'):
        providers.append({'type': LLMProvider.ANTHROPIC, 'key': config['ANTHROPIC_API_KEY'], 'model': 'claude-3-haiku-20240307', 'base_url': 'https://api.anthropic.com/v1', 'cost_per_call': 0.015})
    if config.get('GROQ_API_KEY'):
        providers.append({'type': LLMProvider.GROQ, 'key': config['GROQ_API_KEY'], 'model': 'llama-3.1-8b-instant', 'base_url': 'https://api.groq.com/openai/v1', 'cost_per_call': 0.001})
    if config.get('OPENAI_API_KEY'):
        providers.append({'type': LLMProvider.OPENAI, 'key': config['OPENAI_API_KEY'], 'model': 'gpt-4o', 'base_url': 'https://api.openai.com/v1', 'cost_per_call': 0.01})
    return providers
