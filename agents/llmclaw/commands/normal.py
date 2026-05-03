"""normal - Show normal models menu"""
name = "/normal"

def run(args):
    import json
    from pathlib import Path
    
    models_dir = Path("str(PROJECT_ROOT)/models")
    registry = json.load(open(models_dir / "stock/ollama_registry.json"))
    
    output = ["\n📁 NORMAL MODELS (Ollama)\n" + "="*50]
    for i, model in enumerate(registry.get("models", []), 1):
        output.append(f"  {i}. {model['name']} ({model['size']})")
    
    output.append("\n" + "="*50)
    output.append("Type /use <model_name> to switch")
    
    return "\n".join(output)
