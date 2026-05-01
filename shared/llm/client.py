"""THE SOVEREIGN GATEWAY - Single point of model access."""
import hashlib, asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from .config import load_config
from .response import LLMProvider, ModelTier, AccessDecision, LLMResponse
from .registry import ModelRegistry
from .budget import BudgetController
from .auditor import ChronicleAuditor
from .providers import detect_providers
from .providers.ollama import call_ollama
from .providers.groq import call_groq
from .providers.openrouter import call_openrouter
from .providers.anthropic import call_anthropic
from .providers.openai import call_openai

PROVIDER_CALLERS = {
    LLMProvider.OLLAMA: call_ollama,
    LLMProvider.GROQ: call_groq,
    LLMProvider.OPENROUTER: call_openrouter,
    LLMProvider.ANTHROPIC: call_anthropic,
    LLMProvider.OPENAI: call_openai,
}

_SOVEREIGN_CLIENT = None

def get_llm_client():
    global _SOVEREIGN_CLIENT
    if _SOVEREIGN_CLIENT is None:
        _SOVEREIGN_CLIENT = LLMClient()
    return _SOVEREIGN_CLIENT

class LLMClient:
    def __init__(self):
        self.config = load_config()
        self.providers = detect_providers(self.config)
        self.primary = self.providers[0] if self.providers else None
        self.registry = ModelRegistry()
        self.budget = BudgetController()
        self.auditor = ChronicleAuditor()
        names = [p['type'].value for p in self.providers]
        print(f'LLM Client: {len(self.providers)} providers')
        print(f'Daily budget: {self.budget.daily_budget:.2f}')
        s = self.auditor.get_stats()
        print(f'Chronicle: {s.get("total_interactions", 0)} interactions')
    
    async def call(self, prompt, agent='unknown', model=None, provider=None, max_tokens=4096, temperature=0.7, task_id=None):
        if model is None:
            model = self.registry.get_active_model()
        resolved_model, _ = self.registry.resolve_model(model)
        if model is None:
            model = resolved_model
        if self.budget.check(agent) != AccessDecision.ALLOWED:
            r = LLMResponse(content=f'Budget exceeded for {agent}', provider=LLMProvider.OLLAMA, model='governance', agent=agent, access_decision=AccessDecision.DENIED_BUDGET)
            self.auditor.log(agent, prompt, r)
            return r
        start = datetime.now()
        req_hash = hashlib.sha256(f'{agent}:{prompt}:{start.isoformat()}'.encode()).hexdigest()[:16]
        fallback_used, last_error = False, None
        target = [p for p in self.providers if p['type'] == provider] + [p for p in self.providers if p['type'] != provider] if provider else list(self.providers)
        for prov in target:
            try:
                caller = PROVIDER_CALLERS.get(prov['type'])
                if not caller: continue
                if prov['type'] == LLMProvider.OLLAMA:
                    result = await caller(prov, prompt, max_tokens, temperature, model)
                else:
                    result = await caller(prov, prompt, max_tokens, temperature)
                duration = (datetime.now() - start).total_seconds() * 1000
                response = LLMResponse(content=result['content'], provider=prov['type'], model=prov.get('model', model), agent=agent, tokens_used=result.get('tokens', 0), cost=result.get('cost', prov.get('cost_per_call', 0.001)), duration_ms=duration, access_decision=AccessDecision.ALLOWED, request_hash=req_hash, response_hash=hashlib.sha256(result['content'].encode()).hexdigest()[:16], fallback_used=fallback_used, fallback_provider=str(prov['type'].value) if fallback_used else None)
                self.budget.record(agent, response.cost)
                self.auditor.log(agent, prompt, response)
                return response
            except Exception as e:
                last_error = e
                fallback_used = True
                print(f'{prov["type"].value} failed: {str(e)[:100]}')
                continue
        duration = (datetime.now() - start).total_seconds() * 1000
        r = LLMResponse(content=f'All providers failed: {str(last_error)[:200]}', provider=LLMProvider.OLLAMA, model='governance', agent=agent, duration_ms=duration, access_decision=AccessDecision.DENIED_PROVIDER, request_hash=req_hash, fallback_used=True)
        self.auditor.log(agent, prompt, r)
        return r
    
    def call_sync(self, prompt, agent='unknown', model=None, max_tokens=4096, temperature=0.7, capability=None):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as ex:
                    return ex.submit(asyncio.run, self.call(prompt, agent, model, max_tokens=max_tokens, temperature=temperature)).result(timeout=120)
            return loop.run_until_complete(self.call(prompt, agent, model, max_tokens=max_tokens, temperature=temperature))
        except RuntimeError:
            return asyncio.run(self.call(prompt, agent, model, max_tokens=max_tokens, temperature=temperature))
    
    def get_stats(self):
        s = self.auditor.get_stats()
        b = self.budget.get_stats()
        return {**s, 'budget': b}
    
    def list_models(self, tier=None):
        mt = ModelTier(tier) if tier else None
        return [{'name': m.name, 'provider': m.provider, 'tier': m.tier.value, 'size_gb': m.size_gb, 'is_obliterated': m.is_obliterated} for m in self.registry.list_models(mt)]
    
    def set_active_model(self, name):
        return self.registry.set_active_model(name)
    
    def get_active_model(self):
        return self.registry.get_active_model()

async def generate(prompt, agent='unknown', model=None, provider=None, max_tokens=4096, temperature=0.7):
    return await get_llm_client().call(prompt, agent, model, provider, max_tokens, temperature)

def generate_sync(prompt, agent='unknown', model=None, max_tokens=4096, temperature=0.7):
    return get_llm_client().call_sync(prompt, agent, model, max_tokens, temperature)
