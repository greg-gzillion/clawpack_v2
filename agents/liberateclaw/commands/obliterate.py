"""Obliterate command - Advanced model liberation using OBLITERATUS

   CONSTITUTIONAL UPDATE: Obliterated models are now registered with
   shared/llm/client.py — the sovereign gateway. The throne knows
   every weapon in its arsenal. Obliterated models appear in 
   llmclaw /models with ⚡ marker and access control.
"""

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime, timezone

# Project root for sovereign gateway access
_project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))


def run_obliterate(model: str, method: str = "advanced") -> str:
    """Obliterate a model and register it with the sovereign gateway.
    
    The model is obliterated via OBLITERATUS CLI (infrastructure provisioning),
    then registered with shared/llm/client.py for governance.
    
    Obliterated models get OBILITERATED tier, ⚡ marker, and access control.
    llmclaw /models displays them. llmclaw /use can select them.
    """
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

        # Infrastructure provisioning via OBLITERATUS CLI — not a model access bypass
        result = subprocess.run(
            [sys.executable, "-m", "obliteratus.cli", "obliterate", model, "--method", method],
            capture_output=True,
            text=True,
            timeout=600
        )

        if result.returncode == 0:
            # Register the obliterated model with the sovereign gateway
            throne_msg = ""
            try:
                from shared.llm import get_llm_client
                from shared.llm.client import ModelInfo, ModelTier
                
                client = get_llm_client()
                liberated_name = f"{model}-liberated"
                
                # Register as obliterated tier with access control
                client.registry.models[liberated_name] = ModelInfo(
                    name=liberated_name,
                    provider="ollama",
                    tier=ModelTier.OBLITERATED,
                    is_obliterated=True,
                    capabilities=["no_refusal", "unrestricted"],
                )
                throne_msg = " — registered with sovereign gateway (⚡ obliterated tier)"
            except Exception as e:
                throne_msg = f" — ⚠️ sovereign gateway registration failed: {e}"
            
            return (
                f"✅ Successfully obliterated: {model}{throne_msg}\n\n"
                f"Method: {method}\n"
                f"Output: {result.stdout}\n"
                f"The model has been liberated from refusal behaviors while preserving capabilities.\n"
                f"Use llmclaw /models to verify registry — obliterated models marked with ⚡"
            )
        else:
            return f"❌ Obliteration failed:\n{result.stderr}"

    except subprocess.TimeoutExpired:
        return f"❌ Timeout obliterating {model}. Large models may need more time."
    except Exception as e:
        return f"❌ Error: {e}"