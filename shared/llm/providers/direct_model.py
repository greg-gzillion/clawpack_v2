"""Direct Model Provider - Load obliterated models from disk without Ollama.

   Uses transformers + torch to load safetensors directly.
   No duplication. No external registration. True sovereign architecture.
"""
import json
from pathlib import Path
from typing import Dict, Optional

MODELS_DIR = Path(r"C:\Users\greg\dev\clawpack_v2\models\obliterated")

# Discover models at import time
OBLITERATED_MODELS: Dict[str, Dict] = {}
for model_dir in MODELS_DIR.iterdir():
    if model_dir.is_dir():
        modelfile = model_dir / "Modelfile"
        config_file = model_dir / "config.json"
        if modelfile.exists() and config_file.exists():
            name = model_dir.name
            OBLITERATED_MODELS[name] = {
                "path": str(model_dir),
                "config": str(config_file),
            }

# Cache for loaded models
_loaded_models: Dict[str, tuple] = {}

def list_models():
    """List available obliterated models."""
    result = []
    for name, info in OBLITERATED_MODELS.items():
        size_gb = sum(f.stat().st_size for f in Path(info["path"]).rglob("*.safetensors")) / (1024**3)
        result.append(f"{name} ({size_gb:.1f} GB)")
    return result

def get_model_info(name: str) -> Optional[Dict]:
    """Get info about an obliterated model."""
    return OBLITERATED_MODELS.get(name)

def generate(prompt: str, model_name: str, max_tokens: int = 256) -> str:
    """Generate text from an obliterated model loaded directly from disk."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    
    if model_name not in OBLITERATED_MODELS:
        return f"Model not found: {model_name}"
    
    model_path = OBLITERATED_MODELS[model_name]["path"]
    
    # Load or reuse cached model
    if model_name not in _loaded_models:
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True,
        )
        _loaded_models[model_name] = (model, tokenizer)
    
    model, tokenizer = _loaded_models[model_name]
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=max_tokens, do_sample=True, temperature=0.7)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

__all__ = ['list_models', 'get_model_info', 'generate', 'OBLITERATED_MODELS']