"""use - Switch active model (Ollama + cloud providers)"""
name = "/use"

def run(args):
    import json
    from pathlib import Path

    if not args:
        return "Usage: /use <model_name>"

    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
    models_dir = PROJECT_ROOT / "models"
    config = json.load(open(models_dir / "active_model.json"))
    providers = config.get("providers", {})

    # Cloud providers (fast API-based)
    CLOUD = {
        "groq": {"model": "llama-3.3-70b-versatile", "note": "Free tier, 0.7s"},
        "openrouter": {"model": "google/gemma-4-26b-a4b-it:free", "note": "Free tier, 0.7s"},
        "anthropic": {"model": "claude-haiku-4-5-20251001", "note": "Paid, 1.2s"},
    }

    # Check obliterated models
    obliterated_dir = models_dir / "obliterated"
    obliterated_names = []
    if obliterated_dir.exists():
        for d in obliterated_dir.iterdir():
            if d.is_dir() and (d / "config.json").exists():
                obliterated_names.append(d.name)

    # Check Ollama models
    import subprocess
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    ollama_names = []
    for line in result.stdout.strip().split(chr(10))[1:]:
        parts = line.split()
        if parts:
            ollama_names.append(parts[0])

    def make_priority_one(provider_name, model_name, ptype, note=""):
        config["model"] = model_name
        config["source"] = provider_name
        pconfig = {"model": model_name, "priority": 1, "timeout": 60, "type": ptype}
        if note:
            pconfig["note"] = note
        providers[provider_name] = pconfig
        for p in providers:
            if p != provider_name and providers[p].get("priority", 99) <= 1:
                providers[p]["priority"] = 2
        config["providers"] = providers
        json.dump(config, open(models_dir / "active_model.json", "w"), indent=2)

    # Check cloud providers first
    if args.lower() in CLOUD:
        c = CLOUD[args.lower()]
        make_priority_one(args.lower(), c["model"], "cloud", c["note"])
        return f"Switched to {args} ({c["model"]}) - {c["note"]}"

    # Try obliterated models
    if args in obliterated_names:
        make_priority_one("direct_model", args, "obliterated")
        return f"Switched to obliterated model: {args}"

    # Try Ollama models
    if args in ollama_names:
        make_priority_one("ollama", args, "normal")
        return f"Switched to: {args}"

    # Suggestions
    cloud_names = list(CLOUD.keys())
    all_models = cloud_names + obliterated_names + ollama_names
    matches = [m for m in all_models if args.lower() in m.lower()]
    if matches:
        return f"Not found: {args}\nDid you mean: {chr(44).join(matches[:5])}?"

    return f"Model not found: {args}\nCloud providers: groq, openrouter, anthropic\nUse /models to see local models."
