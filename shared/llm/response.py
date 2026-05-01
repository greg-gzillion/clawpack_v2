"""LLM Response types and enums for the sovereign gateway."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List
from datetime import datetime, timezone


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


__all__ = [
    'LLMProvider', 'ModelTier', 'AccessDecision',
    'ModelInfo', 'LLMResponse',
]
