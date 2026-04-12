"""Use command - Run inference with liberated models"""

import subprocess
from pathlib import Path

LIBERATED_DIR = Path.home() / ".clawpack" / "liberated"

def run_use(model: str, prompt: str) -> str:
    """Use a liberated model for inference"""
    if not model or not prompt:
        return "Usage: /use <model> <prompt>"

    # Try running with Ollama first (most reliable)
    try:
        # SECURE: Use list arguments with shell=False
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=120,
            shell=False  # CRITICAL: Prevents command injection
        )
        if result.returncode == 0:
            return result.stdout.strip()
        elif result.stderr:
            # Return stderr for debugging
            return f"Ollama error: {result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return f"Timeout: {model} took too long to respond"
    except FileNotFoundError:
        return "Ollama not found. Please install Ollama from https://ollama.ai"
    except Exception as e:
        # Fall back to checking if model exists
        pass

    # Check if it's a liberated model
    model_slug = model.replace(':', '_').replace('/', '_')
    model_dir = LIBERATED_DIR / model_slug

    if not model_dir.exists():
        return f"Model {model} not found. Use /liberate {model} first\n\nTry: ollama run {model} \"{prompt}\""

    return f"✅ Model {model} is liberated!\n\nTry running: ollama run {model} \"{prompt}\""
