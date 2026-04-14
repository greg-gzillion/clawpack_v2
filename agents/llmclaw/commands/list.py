"""list - List available models"""
name = "/list"

def run(args):
    import json
    from pathlib import Path
    
    models_dir = Path("C:/Users/greg/dev/clawpack_v2/models")
    active = json.load(open(models_dir / "active_model.json"))
    
    output = ["\n📋 AVAILABLE MODELS\n" + "="*50]
    output.append(f"\n✅ ACTIVE: {active['model']} ({active['source']})")
    
    # Normal models (Ollama)
    output.append("\n📁 NORMAL MODELS (Ollama):")
    registry = json.load(open(models_dir / "stock/ollama_registry.json"))
    for model in registry.get("models", []):
        marker = " ✅" if active['model'] == model['name'] and active['source'] == "stock" else ""
        output.append(f"  • {model['name']} ({model['size']}){marker}")
    
    # Obliterated models
    output.append("\n🔥 OBLITERATED MODELS:")
    obliterated_dir = models_dir / "obliterated"
    for model_dir in obliterated_dir.iterdir():
        if model_dir.is_dir():
            size = sum(f.stat().st_size for f in model_dir.rglob("*.safetensors")) / 1e9
            marker = " ✅" if active['model'] == model_dir.name and active['source'] == "obliterated" else ""
            output.append(f"  • {model_dir.name} ({size:.1f} GB){marker}")
    
    output.append("\n" + "="*50)
    output.append("Use /use <model> to switch models")
    output.append("Use /normal for normal models menu")
    output.append("Use /obliterated for obliterated models menu")
    
    return "\n".join(output)
