"""use - Switch active model"""
name = "/use"

def run(args):
    import json
    import subprocess
    from pathlib import Path

    if not args:
        return "Usage: /use <model_name>\nUse /list to see all models."

    models_dir = Path("C:/Users/greg/dev/clawpack_v2/models")
    config = json.load(open(models_dir / "active_model.json"))
    providers = config.get("providers", {})

    # Build lookup from ollama list
    result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
    ollama_names = []
    for line in result.stdout.strip().split('\n')[1:]:
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
        # Also update the in-memory sovereign gateway singleton
        try:
            from shared.llm.client import get_llm_client
            client = get_llm_client()
            client.registry.set_active_model(model_name)
        except Exception:
            pass

    # 1. Anthropic
    if args in ["claude-haiku-4-5-20251001", "claude-sonnet-4-20250514", "claude-opus-4-20250514"]:
        make_priority_one("anthropic", args, "cloud")
        return f"Switched to Anthropic: {args}"

    # 2. Groq
    if args in ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"]:
        make_priority_one("groq", args, "cloud")
        return f"Switched to Groq: {args}"

    # 3. Obliterated/liberated
    if args in ollama_names and '-liberated' in args:
        make_priority_one("obliterated", args, "obliterated", "No refusals - unrestricted")
        return f"Switched to obliterated: {args}\nUnrestricted - no refusals."

    # 4. Stock Ollama
    if args in ollama_names:
        make_priority_one("ollama", args, "normal")
        return f"Switched to Ollama: {args}"

    # 5. Partial match
    all_known = [
        "claude-haiku-4-5-20251001", "claude-sonnet-4-20250514",
        "llama-3.1-8b-instant",
    ] + ollama_names
    matches = [m for m in all_known if args.lower() in m.lower()]
    if matches:
        return f"Not found: {args}\nDid you mean: {', '.join(matches[:5])}?"

    return f"Model not found: {args}\nUse /list to see all models."
