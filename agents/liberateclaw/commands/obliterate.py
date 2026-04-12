"""Obliterate command - Advanced model liberation using OBLITERATUS"""

import subprocess
import sys
from pathlib import Path

def run_obliterate(model: str, method: str = "advanced") -> str:
    """Obliterate a model using OBLITERATUS (advanced refusal removal)"""
    if not model:
        return """Usage: /obliterate <model> [method]

Methods:
  basic     - Fast baseline (diff-in-means)
  advanced  - Default (norm-preserving, 4 directions)
  surgical  - Precision MoE-aware removal
  nuclear   - Maximum force (all techniques)

Example: /obliterate meta-llama/Llama-3.1-8B-Instruct advanced"""

    # Parse method if provided
    parts = model.split()
    if len(parts) > 1:
        model = parts[0]
        method = parts[1]

    # Check if OBLITERATUS is installed
    try:
        import obliteratus
    except ImportError:
        return """❌ OBLITERATUS not installed.

Install it with:
  pip install git+https://github.com/elder-plinius/OBLITERATUS.git

Or use /liberate for basic Ollama liberation."""

    try:
        print(f"💥 Obliterating {model} using {method} method...")
        print("   This may take several minutes depending on model size.")

        result = subprocess.run(
            [sys.executable, "-m", "obliteratus.cli", "obliterate", model, "--method", method],
            capture_output=True,
            text=True,
            timeout=600
        )

        if result.returncode == 0:
            return f"""✅ Successfully obliterated: {model}

Method: {method}
Output: {result.stdout[:500]}

The model has been liberated from refusal behaviors while preserving capabilities.

Use /liberated to see all available models."""
        else:
            return f"❌ Obliteration failed:\n{result.stderr}"

    except subprocess.TimeoutExpired:
        return f"❌ Timeout obliterating {model}. Large models may need more time."
    except Exception as e:
        return f"❌ Error: {e}"
