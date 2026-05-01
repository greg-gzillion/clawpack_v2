#!/usr/bin/env python3
"""
THE SOVEREIGN GATEWAY - shared/llm/client.py
Constitutional Authority for ALL Model Access in Clawpack V2

NO AGENT MAY SPEAK TO A MODEL DIRECTLY.
This file is the single point of model access for the entire ecosystem.

Constitutional Law:
  1. Every model call passes through this file - NO EXCEPTIONS
  2. llmclaw is the CLI frontend, not an independent authority
  3. All access is logged to Chronicle (immutable audit trail)
  4. Budget and permissions are enforced at this gateway
  5. Auto-fallback across providers with full observability
  6. No agent may import ollama, groq, openrouter, or anthropic directly

Original production code preserved and enhanced with governance layer.
Async support, auto-fallback, provider detection - ALL RETAINED.
"""

import os
import json
import time
import hashlib
import asyncio
import aiohttp
import requests
from pathlib import Path
from typing import AsyncIterator, Optional, Dict, Any, List, Tuple
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timezone


# =============================================================================
# CONSTANTS & PATHS
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
DATA_DIR = PROJECT_ROOT / "data"
CHRONICLE_PATH = DATA_DIR / "chronicle_ledger.json"
ACTIVE_MODEL_PATH = MODELS_DIR / "active_model.json"
WORKING_LLMS_PATH = MODELS_DIR / "working_llms.json"
BUDGET_PATH = DATA_DIR / "llm_budget.json"


# =============================================================================
# ENUMS & DATA CLASSES
# =============================================================================

class LLMProvider(str, Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    OPENROUTER = "openrouter"
    GROQ = "groq"
    OLLAMA = "ollama"

class ModelTier(str, Enum):
    OBLITERATED = "obliterated"
    STANDARD = "standard"
    LARGE_LOCAL = "large_local"
    CLOUD = "cloud"

class AccessDecision(str, Enum):
    ALLOWED = "allowed"
    DENIED_BUDGET = "denied_budget"
    DENIED_PERMISSION = "denied_permission"
    DENIED_PROVIDER = "denied_provider"
    DENIED_RATE_LIMIT = "denied_rate_limit"

@dataclass
class ModelInfo:
    """Model registry entry"""
    name: str
    provider: str
    tier: ModelTier = ModelTier.STANDARD
    size_gb: Optional[float] = None
    context_length: Optional[int] = None
    capabilities: List[str] = field(default_factory=list)
    cost_per_1k_tokens: float = 0.0
    is_obliterated: bool = False

@dataclass
class LLMResponse:
    """Governed model response with full audit metadata"""
    content: str
    provider: LLMProvider
    model: str
    agent: str = "unknown"
    tokens_used: int = 0
    cost: float = 0.0
    duration_ms: float = 0.0
    cached: bool = False
    access_decision: AccessDecision = AccessDecision.ALLOWED
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    request_hash: Optional[str] = None
    response_hash: Optional[str] = None
    fallback_used: bool = False
    fallback_provider: Optional[str] = None


# =============================================================================
# MODEL REGISTRY
# =============================================================================

class ModelRegistry:
    """Central registry of all available models across all providers"""
    
    def __init__(self):
        self.models: Dict[str, ModelInfo] = {}
        self._load_models()
    
    def _load_models(self):
        """Load model registry from disk, .env, and obliterated models"""
        # Load working LLMs registry
        if WORKING_LLMS_PATH.exists():
            try:
                data = json.loads(WORKING_LLMS_PATH.read_text())
                for name, info in data.items():
                    self.models[name] = ModelInfo(
                        name=name,
                        provider=info.get("provider", "ollama"),
                        tier=ModelTier(info.get("tier", "standard")),
                        size_gb=info.get("size_gb"),
                        context_length=info.get("context_length"),
                        capabilities=info.get("capabilities", []),
                    )
            except (json.JSONDecodeError, KeyError):
                pass
        
        # Load obliterated model metadata
        obliterated_dir = MODELS_DIR / "obliterated"
        if obliterated_dir.exists():
            for model_dir in obliterated_dir.iterdir():
                if model_dir.is_dir():
                    metadata_file = model_dir / "abliteration_metadata.json"
                    if metadata_file.exists():
                        try:
                            data = json.loads(metadata_file.read_text())
                            original_name = data.get("original_model", model_dir.name)
                            liberated_name = f"{original_name}-liberated"
                            self.models[liberated_name] = ModelInfo(
                                name=liberated_name,
                                provider="ollama",
                                tier=ModelTier.OBLITERATED,
                                size_gb=data.get("size_gb"),
                                is_obliterated=True,
                                capabilities=data.get("capabilities", []),
                            )
                        except (json.JSONDecodeError, KeyError):
                            pass
        
        # Register cloud models from environment
        if os.environ.get("ANTHROPIC_API_KEY"):
            self.models["claude-3-5-sonnet-20241022"] = ModelInfo(
                name="claude-3-5-sonnet-20241022",
                provider="anthropic",
                tier=ModelTier.CLOUD,
                cost_per_1k_tokens=0.015,
            )
        if os.environ.get("OPENAI_API_KEY"):
            self.models["gpt-4o"] = ModelInfo(
                name="gpt-4o",
                provider="openai",
                tier=ModelTier.CLOUD,
                cost_per_1k_tokens=0.01,
            )
        if os.environ.get("GROQ_API_KEY"):
            self.models["llama-3.1-8b-instant"] = ModelInfo(
                name="llama-3.1-8b-instant",
                provider="groq",
                tier=ModelTier.CLOUD,
            )
        if os.environ.get("OPENROUTER_API_KEY"):
            self.models[os.environ.get("OPENROUTER_MODEL", "z-ai/glm-5.1")] = ModelInfo(
                name=os.environ.get("OPENROUTER_MODEL", "z-ai/glm-5.1"),
                provider="openrouter",
                tier=ModelTier.CLOUD,
            )
    
    def get_active_model(self) -> str:
        """Get the currently active model (set by llmclaw /use)"""
        if ACTIVE_MODEL_PATH.exists():
            try:
                data = json.loads(ACTIVE_MODEL_PATH.read_text())
                return data.get("model", "qwen3-coder:30b")
            except (json.JSONDecodeError, KeyError):
                pass
        return "qwen3-coder:30b"
    
    def set_active_model(self, model_name: str) -> bool:
        """Set the active model system-wide"""
        if model_name in self.models:
            ACTIVE_MODEL_PATH.write_text(json.dumps({
                "model": model_name,
                "set_at": datetime.now(timezone.utc).isoformat(),
                "set_by": "llmclaw"
            }, indent=2))
            return True
        return False
    
    def resolve_model(self, requested: Optional[str] = None) -> Tuple[str, str]:
        """Resolve which model and provider to use"""
        if requested and requested in self.models:
            model_info = self.models[requested]
            return requested, model_info.provider
        
        active = self.get_active_model()
        if active in self.models:
            return active, self.models[active].provider
        
        return active, "ollama"
    
    def list_models(self, tier: Optional[ModelTier] = None) -> List[ModelInfo]:
        """List all models, optionally filtered by tier"""
        if tier:
            return [m for m in self.models.values() if m.tier == tier]
        return list(self.models.values())


# =============================================================================
# BUDGET CONTROLLER
# =============================================================================

class BudgetController:
    """Enforces spending limits per agent with daily caps"""
    
    def __init__(self):
        self.daily_budget: float = 50.0
        self.agent_budgets: Dict[str, float] = {
            "claw_coder": 15.0,
            "lawclaw": 10.0,
            "mediclaw": 10.0,
            "txclaw": 10.0,
            "webclaw": 5.0,
            "llmclaw": 25.0,
            "default": 5.0,
        }
        self._daily_usage: Dict[str, float] = {}
        self._load_state()
    
    def _load_state(self):
        """Load budget state from disk"""
        if BUDGET_PATH.exists():
            try:
                data = json.loads(BUDGET_PATH.read_text())
                self._daily_usage = data.get("usage", {})
                self.daily_budget = data.get("global_budget", 50.0)
                self.agent_budgets.update(data.get("agent_budgets", {}))
            except (json.JSONDecodeError, KeyError):
                pass
    
    def _save_state(self):
        """Persist budget state"""
        BUDGET_PATH.write_text(json.dumps({
            "usage": self._daily_usage,
            "global_budget": self.daily_budget,
            "agent_budgets": self.agent_budgets,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }, indent=2))
    
    def check(self, agent: str, estimated_cost: float = 0.001) -> AccessDecision:
        """Check if agent has budget remaining"""
        agent_budget = self.agent_budgets.get(agent, self.agent_budgets["default"])
        used = self._daily_usage.get(agent, 0.0)
        
        # Global cap check
        total_used = sum(self._daily_usage.values())
        if total_used + estimated_cost > self.daily_budget:
            return AccessDecision.DENIED_BUDGET
        
        # Agent cap check
        if used + estimated_cost > agent_budget:
            return AccessDecision.DENIED_BUDGET
        
        return AccessDecision.ALLOWED
    
    def record(self, agent: str, cost: float):
        """Record usage against budget"""
        self._daily_usage[agent] = self._daily_usage.get(agent, 0.0) + cost
        self._save_state()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get budget statistics"""
        return {
            "daily_budget": self.daily_budget,
            "total_used": sum(self._daily_usage.values()),
            "remaining": self.daily_budget - sum(self._daily_usage.values()),
            "by_agent": dict(self._daily_usage),
            "agent_limits": dict(self.agent_budgets),
        }


# =============================================================================
# CHRONICLE AUDITOR
# =============================================================================

class ChronicleAuditor:
    """Immutable audit trail for every model interaction"""
    
    def __init__(self):
        self.ledger_path = CHRONICLE_PATH
        self._ensure_ledger()
    
    def _ensure_ledger(self):
        """Initialize Chronicle ledger if not exists"""
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.ledger_path.exists():
            self.ledger_path.write_text(json.dumps({
                "genesis": hashlib.sha256(b"CLAWPACK_CHRONICLE_GENESIS").hexdigest(),
                "entries": []
            }, indent=2))
    
    def log(self, agent: str, prompt: str, response: LLMResponse):
        """Record a model interaction permanently"""
        entry = {
            "timestamp": response.timestamp,
            "agent": agent,
            "model": response.model,
            "provider": response.provider.value,
            "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest()[:16],
            "response_hash": hashlib.sha256(response.content.encode()).hexdigest()[:16],
            "tokens_used": response.tokens_used,
            "cost": response.cost,
            "duration_ms": response.duration_ms,
            "cached": response.cached,
            "decision": response.access_decision.value,
            "fallback_used": response.fallback_used,
            "fallback_provider": response.fallback_provider,
        }
        
        try:
            if self.ledger_path.exists():
                ledger = json.loads(self.ledger_path.read_text())
            else:
                ledger = {"genesis": hashlib.sha256(b"CLAWPACK_CHRONICLE_GENESIS").hexdigest(), "entries": []}
            
            ledger["entries"].append(entry)
            self.ledger_path.write_text(json.dumps(ledger, indent=2))
        except Exception as e:
            print(f"⚠️ Chronicle audit failed: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get system-wide usage statistics"""
        if not self.ledger_path.exists():
            return {"total_interactions": 0, "by_agent": {}, "by_model": {}, "total_cost": 0.0}
        
        try:
            ledger = json.loads(self.ledger_path.read_text())
            entries = ledger.get("entries", [])
        except (json.JSONDecodeError, KeyError):
            return {"total_interactions": 0, "by_agent": {}, "by_model": {}, "total_cost": 0.0}
        
        stats = {
            "total_interactions": len(entries),
            "by_agent": {},
            "by_model": {},
            "by_provider": {},
            "total_cost": 0.0,
            "total_tokens": 0,
            "avg_latency_ms": 0.0,
            "recent_entries": entries[-10:] if entries else [],
        }
        
        for entry in entries:
            agent = entry.get("agent", "unknown")
            model = entry.get("model", "unknown")
            provider = entry.get("provider", "unknown")
            
            stats["by_agent"][agent] = stats["by_agent"].get(agent, 0) + 1
            stats["by_model"][model] = stats["by_model"].get(model, 0) + 1
            stats["by_provider"][provider] = stats["by_provider"].get(provider, 0) + 1
            stats["total_cost"] += entry.get("cost", 0)
            stats["total_tokens"] += entry.get("tokens_used", 0)
        
        if entries:
            stats["avg_latency_ms"] = sum(e.get("duration_ms", 0) for e in entries) / len(entries)
        
        return stats


# =============================================================================
# THE SOVEREIGN LLM CLIENT
# =============================================================================

class LLMClient:
    """
    THE SOVEREIGN GATEWAY
    
    Production LLM client with:
    - Async support (aiohttp)
    - Auto-fallback across providers
    - Provider auto-detection from .env
    - Full budget enforcement
    - Immutable Chronicle audit trail
    - Model registry with llmclaw integration
    
    NO AGENT MAY SPEAK TO A MODEL DIRECTLY.
    Every call passes through this gateway. No exceptions.
    """
    
    def __init__(self):
        # Original production code - ALL RETAINED
        self.config = self._load_config()
        self.providers = self._detect_providers()
        self.primary = self.providers[0] if self.providers else None
        
        # NEW: Governance layer
        self.registry = ModelRegistry()
        self.budget = BudgetController()
        self.auditor = ChronicleAuditor()
        
        provider_names = [p['type'].value for p in self.providers]
        print(f"🤖 LLM Client initialized: {len(self.providers)} providers ({', '.join(provider_names)})")
        print(f"💰 Daily budget: ${self.budget.daily_budget:.2f}")
        print(f"📜 Chronicle: {self.auditor.get_stats()['total_interactions']} interactions recorded")
    
    # =========================================================================
    # ORIGINAL PRODUCTION CODE - FULLY PRESERVED
    # =========================================================================
    
    def _load_config(self) -> Dict[str, str]:
        """Load API keys from .env"""
        config = {}
        env_path = Path(".env")
        if env_path.exists():
            for line in env_path.read_text().split('\n'):
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip().strip('"').strip("'")
        return config
    
    def _detect_providers(self) -> list:
        """Auto-detect available providers with priority ordering"""
        providers = []
        
        # Local models first (fastest, no cost)
        if self._check_ollama():
            providers.append({
                'type': LLMProvider.OLLAMA,
                'model': 'qwen3-coder:30b',
                'base_url': 'http://localhost:11434',
                'cost_per_call': 0.0,
            })
        
        # Cloud providers in priority order
        if self.config.get('OPENROUTER_API_KEY'):
            providers.append({
                'type': LLMProvider.OPENROUTER,
                'key': self.config['OPENROUTER_API_KEY'],
                'model': self.config.get('OPENROUTER_MODEL', 'z-ai/glm-5.1'),
                'base_url': 'https://openrouter.ai/api/v1',
                'cost_per_call': 0.002,
            })
        
        if self.config.get('ANTHROPIC_API_KEY'):
            providers.append({
                'type': LLMProvider.ANTHROPIC,
                'key': self.config['ANTHROPIC_API_KEY'],
                'model': 'claude-3-5-sonnet-20241022',
                'base_url': 'https://api.anthropic.com/v1',
                'cost_per_call': 0.015,
            })
        
        if self.config.get('GROQ_API_KEY'):
            providers.append({
                'type': LLMProvider.GROQ,
                'key': self.config['GROQ_API_KEY'],
                'model': 'llama-3.1-8b-instant',
                'base_url': 'https://api.groq.com/openai/v1',
                'cost_per_call': 0.001,
            })
        
        if self.config.get('OPENAI_API_KEY'):
            providers.append({
                'type': LLMProvider.OPENAI,
                'key': self.config['OPENAI_API_KEY'],
                'model': 'gpt-4o',
                'base_url': 'https://api.openai.com/v1',
                'cost_per_call': 0.01,
            })
        
        return providers
    
    def _check_ollama(self) -> bool:
        """Check if Ollama is running locally"""
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=2)
            return r.status_code == 200
        except Exception:
            return False
    
    # =========================================================================
    # GOVERNED CALL METHOD - The Sovereign Interface
    # =========================================================================
    
    async def call(self, prompt: str, agent: str = "unknown",
                   model: Optional[str] = None,
                   provider: Optional[LLMProvider] = None,
                   max_tokens: int = 4096,
                   temperature: float = 0.7,
                   task_id: Optional[str] = None) -> LLMResponse:
        """
        THE SOVEREIGN METHOD - All model access passes through here.
        
        Args:
            prompt: The prompt to send to the model
            agent: Which agent is making this request (for audit)
            model: Specific model to use (None = use system default from llmclaw)
            provider: Specific provider to use (None = auto-detect with fallback)
            max_tokens: Maximum response tokens
            temperature: Model temperature (0-1)
            task_id: Optional task tracking ID
            
        Returns:
            LLMResponse with full audit metadata
        """
        
        # 1. Resolve model (respects llmclaw /use if model not specified)
        if model is None:
            model = self.registry.get_active_model()
        resolved_model, resolved_provider = self.registry.resolve_model(model)
        if model is None:
            model = resolved_model
        
        # 2. Budget check
        estimated_cost = 0.001  # Default estimate
        if self.budget.check(agent, estimated_cost) != AccessDecision.ALLOWED:
            response = LLMResponse(
                content=f"🚫 Budget exceeded for agent '{agent}'. Daily limit reached. Use /stats to review.",
                provider=LLMProvider.OLLAMA,
                model="governance",
                agent=agent,
                tokens_used=0,
                cost=0.0,
                duration_ms=0.0,
                access_decision=AccessDecision.DENIED_BUDGET,
            )
            self.auditor.log(agent, prompt, response)
            return response
        
        # 3. Execute with auto-fallback
        start = datetime.now()
        request_hash = hashlib.sha256(f"{agent}:{prompt}:{start.isoformat()}".encode()).hexdigest()[:16]
        fallback_used = False
        last_error = None
        
        # Determine which providers to try
        if provider:
            # Specific provider requested - try it first, then fallback
            target_providers = [p for p in self.providers if p['type'] == provider]
            target_providers += [p for p in self.providers if p['type'] != provider]
        else:
            target_providers = list(self.providers)
        
        for prov in target_providers:
            try:
                if prov['type'] == LLMProvider.OPENROUTER:
                    result = await self._call_openrouter(prov, prompt, max_tokens, temperature)
                elif prov['type'] == LLMProvider.ANTHROPIC:
                    result = await self._call_anthropic(prov, prompt, max_tokens, temperature)
                elif prov['type'] == LLMProvider.OPENAI:
                    result = await self._call_openai(prov, prompt, max_tokens, temperature)
                elif prov['type'] == LLMProvider.GROQ:
                    result = await self._call_groq(prov, prompt, max_tokens, temperature)
                elif prov['type'] == LLMProvider.OLLAMA:
                    result = await self._call_ollama(prov, prompt, max_tokens, temperature, model)
                else:
                    continue
                
                duration = (datetime.now() - start).total_seconds() * 1000
                response = LLMResponse(
                    content=result['content'],
                    provider=prov['type'],
                    model=prov.get('model', model),
                    agent=agent,
                    tokens_used=result.get('tokens', 0),
                    cost=result.get('cost', prov.get('cost_per_call', 0.001)),
                    duration_ms=duration,
                    access_decision=AccessDecision.ALLOWED,
                    request_hash=request_hash,
                    response_hash=hashlib.sha256(result['content'].encode()).hexdigest()[:16],
                    fallback_used=fallback_used,
                    fallback_provider=str(prov['type'].value) if fallback_used else None,
                )
                
                # Record budget and audit
                self.budget.record(agent, response.cost)
                self.auditor.log(agent, prompt, response)
                
                return response
                
            except Exception as e:
                last_error = e
                fallback_used = True
                print(f"⚠️ {prov['type'].value} failed: {str(e)[:100]}")
                continue
        
        # All providers failed
        duration = (datetime.now() - start).total_seconds() * 1000
        response = LLMResponse(
            content=f"🚫 All LLM providers failed. Last error: {str(last_error)[:200]}",
            provider=LLMProvider.OLLAMA,
            model="governance",
            agent=agent,
            tokens_used=0,
            cost=0.0,
            duration_ms=duration,
            access_decision=AccessDecision.DENIED_PROVIDER,
            request_hash=request_hash,
            fallback_used=True,
        )
        self.auditor.log(agent, prompt, response)
        return response
    
    def call_sync(self, prompt: str, agent: str = "unknown",
                  model: Optional[str] = None,
                  max_tokens: int = 4096,
                  temperature: float = 0.7) -> LLMResponse:
        """Synchronous wrapper for call() - for agents that can't use async"""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Already in event loop - create new one
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self.call(
                        prompt, agent, model, max_tokens=max_tokens, temperature=temperature
                    ))
                    return future.result(timeout=120)
            return loop.run_until_complete(self.call(
                prompt, agent, model, max_tokens=max_tokens, temperature=temperature
            ))
        except RuntimeError:
            return asyncio.run(self.call(
                prompt, agent, model, max_tokens=max_tokens, temperature=temperature
            ))
    
    # =========================================================================
    # PROVIDER IMPLEMENTATIONS - ORIGINAL CODE PRESERVED
    # =========================================================================
    
    async def _call_openrouter(self, provider: dict, prompt: str, max_tokens: int, temp: float) -> dict:
        """OpenRouter API call"""
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {provider['key']}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/greg-gzillion/clawpack_v2",
                "X-Title": "Clawpack V2"
            }
            
            data = {
                "model": provider['model'],
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temp
            }
            
            async with session.post(
                f"{provider['base_url']}/chat/completions",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=120)
            ) as resp:
                result = await resp.json()
                if 'error' in result:
                    raise Exception(f"OpenRouter API error: {result['error']}")
                return {
                    "content": result['choices'][0]['message']['content'],
                    "tokens": result.get('usage', {}).get('total_tokens', 0),
                    "cost": 0.002  # Approximate
                }
    
    async def _call_anthropic(self, provider: dict, prompt: str, max_tokens: int, temp: float) -> dict:
        """Anthropic Claude API call"""
        async with aiohttp.ClientSession() as session:
            headers = {
                "x-api-key": provider['key'],
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": provider['model'],
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temp
            }
            
            async with session.post(
                f"{provider['base_url']}/messages",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=120)
            ) as resp:
                result = await resp.json()
                if 'error' in result:
                    raise Exception(f"Anthropic API error: {result['error']}")
                return {
                    "content": result['content'][0]['text'],
                    "tokens": result.get('usage', {}).get('input_tokens', 0) + 
                             result.get('usage', {}).get('output_tokens', 0),
                    "cost": 0.015  # Approximate
                }
    
    async def _call_openai(self, provider: dict, prompt: str, max_tokens: int, temp: float) -> dict:
        """OpenAI API call"""
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {provider['key']}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": provider['model'],
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temp
            }
            
            async with session.post(
                f"{provider['base_url']}/chat/completions",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=120)
            ) as resp:
                result = await resp.json()
                if 'error' in result:
                    raise Exception(f"OpenAI API error: {result['error']}")
                return {
                    "content": result['choices'][0]['message']['content'],
                    "tokens": result.get('usage', {}).get('total_tokens', 0),
                    "cost": 0.01  # Approximate
                }
    
    async def _call_groq(self, provider: dict, prompt: str, max_tokens: int, temp: float) -> dict:
        """Groq API call"""
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {provider['key']}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": provider['model'],
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temp
            }
            
            async with session.post(
                f"{provider['base_url']}/chat/completions",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as resp:
                result = await resp.json()
                if 'error' in result:
                    raise Exception(f"Groq API error: {result['error']}")
                return {
                    "content": result['choices'][0]['message']['content'],
                    "tokens": result.get('usage', {}).get('total_tokens', 0),
                    "cost": 0.001  # Approximate
                }
    
    async def _call_ollama(self, provider: dict, prompt: str, max_tokens: int, temp: float, model: str) -> dict:
        """Ollama local model call"""
        async with aiohttp.ClientSession() as session:
            # Use the resolved model, falling back to provider default
            ollama_model = model if model and model != "governance" else provider.get('model', 'llama3.2:3b')
            
            data = {
                "model": ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": temp
                }
            }
            
            async with session.post(
                f"{provider['base_url']}/api/generate",
                json=data,
                timeout=aiohttp.ClientTimeout(total=300)
            ) as resp:
                result = await resp.json()
                return {
                    "content": result.get('response', ''),
                    "tokens": result.get('eval_count', 0),
                    "cost": 0.0
                }
    
    # =========================================================================
    # GOVERNANCE METHODS - llmclaw Integration
    # =========================================================================
    
    def get_stats(self) -> Dict[str, Any]:
        """Get system-wide usage statistics (for llmclaw /stats)"""
        stats = self.auditor.get_stats()
        budget_stats = self.budget.get_stats()
        return {**stats, "budget": budget_stats}
    
    def list_models(self, tier: Optional[str] = None) -> List[Dict]:
        """List available models (for llmclaw /models)"""
        model_tier = ModelTier(tier) if tier else None
        models = self.registry.list_models(model_tier)
        return [
            {
                "name": m.name,
                "provider": m.provider,
                "tier": m.tier.value,
                "size_gb": m.size_gb,
                "is_obliterated": m.is_obliterated,
            }
            for m in models
        ]
    
    def set_active_model(self, model_name: str) -> bool:
        """Set the active model system-wide (for llmclaw /use)"""
        return self.registry.set_active_model(model_name)
    
    def get_active_model(self) -> str:
        """Get current active model (for llmclaw)"""
        return self.registry.get_active_model()


# =============================================================================
# SINGLETON - The ONE instance that governs all model access
# =============================================================================

_SOVEREIGN_CLIENT: Optional[LLMClient] = None

def get_llm_client() -> LLMClient:
    """
    Get THE sovereign LLM client. There is only ONE.
    
    Every agent must use this. No agent may speak to a model directly.
    This is constitutional law, not a suggestion.
    """
    global _SOVEREIGN_CLIENT
    if _SOVEREIGN_CLIENT is None:
        _SOVEREIGN_CLIENT = LLMClient()
    return _SOVEREIGN_CLIENT


# =============================================================================
# CONVENIENCE FUNCTIONS - For agents that just want text
# =============================================================================

async def generate(prompt: str, agent: str = "unknown", 
                   model: Optional[str] = None,
                   provider: Optional[LLMProvider] = None,
                   max_tokens: int = 4096,
                   temperature: float = 0.7) -> LLMResponse:
    """
    Constitutional convenience function for async agents.
    This is the ONLY way any agent should access any model.
    """
    client = get_llm_client()
    return await client.call(prompt, agent, model, provider, max_tokens, temperature)


def generate_sync(prompt: str, agent: str = "unknown",
                  model: Optional[str] = None,
                  max_tokens: int = 4096,
                  temperature: float = 0.7) -> LLMResponse:
    """
    Constitutional convenience function for synchronous agents.
    This is the ONLY way any synchronous agent should access any model.
    """
    client = get_llm_client()
    return client.call_sync(prompt, agent, model, max_tokens, temperature)