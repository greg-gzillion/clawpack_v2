"""List liberated models"""

from pathlib import Path

LIBERATED_DIR = Path.home() / ".clawpack" / "liberated"

def list_liberated() -> str:
    """List all liberated models"""
    if not LIBERATED_DIR.exists():
        return "No liberated models yet. Use /liberate <model> or /obliterate <model>"

    models = list(LIBERATED_DIR.iterdir())

    if not models:
        return "No liberated models yet. Use /liberate <model> or /obliterate <model>"

    output = f"🔓 Liberated Models ({len(models)}):\n"
    output += "─" * 40 + "\n"

    for m in sorted(models):
        if m.is_dir():
            info_file = m / "info.json"
            if info_file.exists():
                import json
                info = json.loads(info_file.read_text())
                model_name = info.get("model", m.name)
                method = info.get("method", "unknown")
                output += f"  📦 {model_name}\n     Method: {method}\n"
            else:
                output += f"  📦 {m.name}\n"

    return output
