"""use - Switch active model"""
name = "/use"

def run(args):
    import json
    import subprocess
    from pathlib import Path

    if not args:
        return "Usage: /use <model_name>"

    models_dir = Path("C:/Users/greg/dev/clawpack_v2/models")
    config = json.load(open(models_dir / "active_model.json"))
    providers = config.get("providers", {})

    result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
    ollama_names = []
    for line in result.stdout.strip().split(chr(10))[1:]:
        parts = line.split()
        if parts: ollama_names.append(parts[0])

    def make_priority_one(provider_name, model_name, ptype, note=""):
        config["model"] = model_name
        config["source"] = provider_name
        pconfig = {"model": model_name, "priority": 1, "timeout": 60, "type": ptype}
        if note: pconfig["note"] = note
        providers[provider_name] = pconfig
        for p in providers:
            if p != provider_name and providers[p].get("priority", 99) <= 1:
                providers[p]["priority"] = 2
        config["providers"] = providers
        json.dump(config, open(models_dir / "active_model.json", "w"), indent=2)

    if args in ollama_names:
        make_priority_one("ollama", args, "normal")
        return f"Switched to: {args}"

    matches = [m for m in ollama_names if args.lower() in m.lower()]
    if matches:
        return f"Not found: {args}\nDid you mean: {chr(44).join(matches[:5])}?"

    return f"Model not found: {args}"