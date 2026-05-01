"""LLM Provider System - THE SOVEREIGN GATEWAY"""
from .client import LLMClient, get_llm_client, generate, generate_sync
from .response import LLMResponse, AccessDecision, ModelTier, LLMProvider
from .ollama import OllamaProvider
from .openrouter import OpenRouterProvider
from .anthropic import AnthropicProvider
from .manager import LLMManager

def generate_simple(prompt, agent='unknown', model=None, max_tokens=4096, temperature=0.7):
    return get_llm_client().call_sync(prompt=prompt, agent=agent, model=model, max_tokens=max_tokens, temperature=temperature)

__all__ = ['LLMClient', 'get_llm_client', 'generate', 'generate_sync', 'generate_simple', 'LLMResponse', 'AccessDecision', 'ModelTier', 'LLMProvider', 'OllamaProvider', 'OpenRouterProvider', 'AnthropicProvider', 'LLMManager']
