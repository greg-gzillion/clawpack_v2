"""use - Switch active model"""
name = "/use"

def run(args):
    import json
    from pathlib import Path
    
    if not args:
        return "Usage: /use <model_name>"
    
    models_dir = Path("C:/Users/greg/dev/clawpack_v2/models")
    
    # Check obliterated first
    obliterated_dir = models_dir / "obliterated"
    for model_dir in obliterated_dir.iterdir():
        if model_dir.is_dir() and model_dir.name.lower() == args.lower():
            config = {"model": model_dir.name, "source": "obliterated"}
            json.dump(config, open(models_dir / "active_model.json", "w"))
            return f"✅ Switched to obliterated model: {model_dir.name}"
    
    # Check normal models
    registry = json.load(open(models_dir / "stock/ollama_registry.json"))
    for model in registry.get("models", []):
        if model['name'].lower() == args.lower():
            config = {"model": model['name'], "source": "stock"}
            json.dump(config, open(models_dir / "active_model.json", "w"))
            return f"✅ Switched to normal model: {model['name']}"
    
    return f"❌ Model not found: {args}\nUse /list to see available models"
