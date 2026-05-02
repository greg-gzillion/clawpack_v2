"""LLM Router - Centralized dispatch logic for all model access.

   Constitutional principle: The empire decides which model serves which task.
   Not probabilistic. Deterministic. Strategic.

   Priority:
   - Cloud models (Anthropic, Groq) for orchestration, planning, complex tasks
   - Obliterated local models for generation, code, unrestricted content
"""
from typing import Optional, Dict

# Task types that should use local obliterated models
LOCAL_TASK_TYPES = {
    "code_generation",
    "code_drafting", 
    "private_reasoning",
    "sensitive_analysis",
    "restricted_content",
    "raw_generation",
    "uncensored_response",
    "direct_inference",
}

# Task types that should use cloud models
CLOUD_TASK_TYPES = {
    "code_generation",
    "code_drafting",
    "orchestration",
    "planning",
    "agent_routing",
    "multi_step_reasoning",
    "verification",
    "summarization",
    "translation",
    "law_analysis",
    "medical_analysis",
    "raw_generation",
    "direct_inference",
}

def route(capability: str = None, task_type: str = None) -> str:
    """Determine which provider to use based on task type.
    
    Returns provider name: 'anthropic', 'groq', 'direct_model', or None for default priority.
    """
    if task_type in LOCAL_TASK_TYPES:
        return "direct_model"
    if task_type in ("code_generation", "code_drafting"):
        return "anthropic"
    if task_type in CLOUD_TASK_TYPES:
        return "anthropic"
    # Default: use priority-based fallback
    return None

PROVIDER_PRIORITY = {
    "code_generation": ["anthropic", "groq"],
    "orchestration": ["anthropic", "groq"],
    "private": ["direct_model"],
    "default": ["anthropic", "groq", "direct_model"],
}

def get_provider_list(mode: str = "default") -> list:
    """Get ordered provider list for a given mode."""
    return PROVIDER_PRIORITY.get(mode, PROVIDER_PRIORITY["default"])

__all__ = ['route', 'get_provider_list', 'LOCAL_TASK_TYPES', 'CLOUD_TASK_TYPES']