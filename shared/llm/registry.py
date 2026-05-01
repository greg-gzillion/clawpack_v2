"""Model Registry — central catalog of all available models."""

import json
import os
from pathlib import Path
from typing import Dict, Optional, List, Tuple

from .config import WORKING_LLMS_PATH, MODELS_DIR, ACTIVE_MODEL_PATH
from .response import ModelInfo, ModelTier


class ModelRegistry:
    """Central registry of all available models across all providers"""
    
    def __init__(self):
        self.models: Dict[str, ModelInfo] = {}
        self._load_models()
    
    def _load_models(self):
        """Load model registry from disk, .env, and obliterated models"""
        if WORKING_LLMS_PATH.exists():
            try:
                data = json.loads(WORKING_LLMS_PATH.read_text())
                if isinstance(data, list):
                    for entry in data:
                        name = entry.get('model', entry.get('name', 'unknown'))
                        size_str = entry.get('size', '0 GB')
                        size_gb = None
                        if size_str:
                            size_str = size_str.replace(' GB','').replace(' MB','').strip()
                            try:
                                size_gb = float(size_str) / (1024 if 'MB' in entry.get('size','') else 1)
                            except ValueError:
                                pass
                        self.models[name] = ModelInfo(
                            name=name,
                            provider=entry.get('source', entry.get('provider', 'ollama')),
                            tier=ModelTier.OBLITERATED if entry.get('obliterated') else ModelTier.STANDARD,
                            size_gb=size_gb,
                            is_obliterated=entry.get('obliterated', False),
                        )
                elif isinstance(data, dict):
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
            self.models["claude-3-haiku-20240307"] = ModelInfo(
                name="claude-3-haiku-20240307",
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
        if ACTIVE_MODEL_PATH.exists():
            try:
                data = json.loads(ACTIVE_MODEL_PATH.read_text())
                return data.get("model", "qwen3-coder:30b")
            except (json.JSONDecodeError, KeyError):
                pass
        return "qwen3-coder:30b"
    
    def set_active_model(self, model_name: str) -> bool:
        if model_name in self.models:
            from datetime import datetime, timezone
            ACTIVE_MODEL_PATH.write_text(json.dumps({
                "model": model_name,
                "set_at": datetime.now(timezone.utc).isoformat(),
                "set_by": "llmclaw"
            }, indent=2))
            return True
        return False
    
    def resolve_model(self, requested: Optional[str] = None) -> Tuple[str, str]:
        if requested and requested in self.models:
            return requested, self.models[requested].provider
        active = self.get_active_model()
        if active in self.models:
            return active, self.models[active].provider
        return active, "ollama"
    
    def list_models(self, tier: Optional[ModelTier] = None) -> List[ModelInfo]:
        if tier:
            return [m for m in self.models.values() if m.tier == tier]
        return list(self.models.values())


__all__ = ['ModelRegistry']
