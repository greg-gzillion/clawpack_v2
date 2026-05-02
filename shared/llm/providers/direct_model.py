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

def generate(prompt: str, model_name: str, max_tokens: int = 128) -> str:
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
            dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True,
        )
        _loaded_models[model_name] = (model, tokenizer)
    
    model, tokenizer = _loaded_models[model_name]
    
    # Direct prompt formatting - base models don't need chat templates
    # Just wrap in a simple instruction format if it looks like a request
    if any(kw in prompt.lower() for kw in ['write', 'generate', 'create', 'code', 'function', 'class']):
        formatted = prompt  # Direct prompt for code generation
    else:
        formatted = prompt
    inputs = tokenizer(formatted, return_tensors="pt").to(model.device)
    
    import torch
    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            use_cache=True,
        )
    
    # Decode with proper spacing and character cleanup
    full_output = tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
    # Strip the input prompt from output
    if full_output.startswith(prompt):
        full_output = full_output[len(prompt):].strip()
    elif formatted != prompt and full_output.startswith(formatted):
        full_output = full_output[len(formatted):].strip()
    full_output = full_output.replace(chr(288)+chr(138), chr(10)).replace(chr(288)+chr(160), chr(32))
    full_output = full_output.replace(chr(288)+chr(138), chr(10)).replace(chr(288)+chr(160), chr(32))
    return full_output
__all__ = ['list_models', 'get_model_info', 'generate', 'OBLITERATED_MODELS']