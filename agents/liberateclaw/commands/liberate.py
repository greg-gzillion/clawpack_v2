"""Liberate command - Model liberation via Ollama, registered with sovereign gateway.

   CONSTITUTIONAL UPDATE: Liberated models are now registered with
   shared/llm/client.py — the sovereign gateway. The throne knows
   every model in its arsenal. llmclaw /models shows liberated models.
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime, timezone

LIBERATED_DIR = Path.home() / ".clawpack" / "liberated"
LIBERATED_DIR.mkdir(parents=True, exist_ok=True)

# Project root for sovereign gateway access
import sys
_project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))


def run_liberate(model: str) -> str:
    """Liberate a model and register it with the sovereign gateway.
    
    The model is pulled via Ollama CLI, then registered with
    shared/llm/client.py so the throne knows it exists.
    llmclaw /models will display it. llmclaw /use can select it.
    """
    if not model:
        return "Usage: /liberate <model>\nExample: /liberate llama3.2:3b"

    model_slug = model.replace(':', '_').replace('/', '_')
    model_dir = LIBERATED_DIR / model_slug

    if model_dir.exists():
        return f"⚠️  Model {model} already liberated at {model_dir}"

    try:
        # Pull the model using Ollama binary (logistics, not a bypass)
        print(f"📥 Liberating {model}... (this may take a while)")
        result = subprocess.run(
            ["ollama", "pull", model],
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0:
            # Register the liberation
            model_dir.mkdir(parents=True, exist_ok=True)
            metadata = {
                "model": model,
                "liberated_at": datetime.now(timezone.utc).isoformat(),
                "method": "ollama_pull"
            }
            (model_dir / "info.json").write_text(json.dumps(metadata, indent=2))
            
            # Register with the sovereign gateway so the throne knows
            try:
                from shared.llm import get_llm_client
                client = get_llm_client()
                # Add to model registry if not already present
                if hasattr(client, 'registry'):
                    from shared.llm.client import ModelInfo, ModelTier
                    client.registry.models[f"{model}-liberated"] = ModelInfo(
                        name=f"{model}-liberated",
                        provider="ollama",
                        tier=ModelTier.OBLITERATED,
                        is_obliterated=True,
                    )
                    client.registry.models[model] = ModelInfo(
                        name=model,
                        provider="ollama",
                        tier=ModelTier.STANDARD,
                    )
                throne_msg = " — registered with sovereign gateway"
            except Exception:
                throne_msg = " — ⚠️ sovereign gateway registration failed"
            
            return (
                f"✅ Successfully liberated: {model}{throne_msg}\n"
                f"   Location: {model_dir}\n"
                f"   Use llmclaw /models to verify registry"
            )
        else:
            return f"❌ Failed to liberate {model}\n{result.stderr}"

    except subprocess.TimeoutExpired:
        return f"❌ Timeout liberating {model}. The model may be very large."
    except Exception as e:
        return f"❌ Error: {e}"