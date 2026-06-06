"""list - List all available models (local + cloud)"""
name = "/list"

def run(args):
    import subprocess, json
    from pathlib import Path

    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
    models_dir = PROJECT_ROOT / "models"
    config = json.load(open(models_dir / "active_model.json"))

    lines = []
    lines.append("\n" + "="*60)
    lines.append("  ALL MODELS")
    lines.append("="*60)
    lines.append(f"  ACTIVE: {config["model"]} ({config["source"]})")

    # Cloud providers
    CLOUD = {
        "groq": "llama-3.3-70b-versatile (Free, 0.7s)",
        "openrouter": "google/gemma-4-26b-a4b-it:free (Free, 0.7s)",
        "anthropic": "claude-haiku-4-5-20251001 (Paid, 1.2s)",
    }
    lines.append("\n  CLOUD PROVIDERS:")
    for name, desc in CLOUD.items():
        mark = " [ACTIVE]" if config["source"] == name else ""
        lines.append(f"    {name}: {desc}{mark}")

    # Get Ollama models
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    ollama_models = []
    if result.returncode == 0:
        for line in result.stdout.strip().split(chr(10))[1:]:
            parts = line.split()
            if parts:
                name = parts[0]
                size = parts[1] + " " + parts[2] if len(parts) > 2 else ""
                ollama_models.append((name, size))

    obliterated = [(n, s) for n, s in ollama_models if "-liberated" in n]
    stock = [(n, s) for n, s in ollama_models if "-liberated" not in n]

    if obliterated:
        lines.append("\n  OBLITERATED:")
        for name, size in obliterated:
            mark = " [ACTIVE]" if config["model"] == name else ""
            lines.append(f"    {name}  {size}{mark}")

    if stock:
        lines.append("\n  LOCAL (OLLAMA):")
        for name, size in stock:
            mark = " [ACTIVE]" if config["model"] == name else ""
            lines.append(f"    {name}  {size}{mark}")

    # Priority chain
    providers = config.get("providers", {})
    lines.append("\n" + "-"*60)
    lines.append("  PROVIDER CHAIN:")
    sorted_p = sorted(providers.items(), key=lambda x: x[1].get("priority", 99))
    for i, (name, pconfig) in enumerate(sorted_p, 1):
        lines.append(f"    {i}. {name}: {pconfig.get("model", "?")}")

    lines.append("\n" + "="*60)
    lines.append("  /use groq | /use openrouter | /use anthropic")
    lines.append("  /use <model_name> for local models")
    return "\n".join(lines)
