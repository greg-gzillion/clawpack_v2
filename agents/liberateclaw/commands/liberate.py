"""Liberate command - Local model liberation via Ollama"""

import subprocess
import json
from pathlib import Path
from datetime import datetime

LIBERATED_DIR = Path.home() / ".clawpack" / "liberated"
LIBERATED_DIR.mkdir(parents=True, exist_ok=True)

def run_liberate(model: str) -> str:
    """Liberate a model using Ollama"""
    if not model:
        return "Usage: /liberate <model>\nExample: /liberate llama3.2:3b"

    model_slug = model.replace(':', '_').replace('/', '_')
    model_dir = LIBERATED_DIR / model_slug

    if model_dir.exists():
        return f"⚠️  Model {model} already liberated at {model_dir}"

    try:
        # Pull the model using Ollama
        print(f"📥 Liberating {model}... (this may take a while)")
        result = subprocess.run(
            ["ollama", "pull", model],
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0:
            model_dir.mkdir(parents=True, exist_ok=True)
            (model_dir / "info.json").write_text(json.dumps({
                "model": model,
                "liberated_at": datetime.now().isoformat(),
                "method": "ollama_pull"
            }, indent=2))
            return f"✅ Successfully liberated: {model}\n   Location: {model_dir}"
        else:
            return f"❌ Failed to liberate {model}\n{result.stderr}"

    except subprocess.TimeoutExpired:
        return f"❌ Timeout liberating {model}. The model may be very large."
    except Exception as e:
        return f"❌ Error: {e}"
