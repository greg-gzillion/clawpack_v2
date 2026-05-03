"""obliterated - Show obliterated models menu"""
name = "/obliterated"

def run(args):
    from pathlib import Path
    
    models_dir = Path("str(PROJECT_ROOT)/models")
    obliterated_dir = models_dir / "obliterated"
    
    output = ["\n🔥 OBLITERATED MODELS\n" + "="*50]
    models = []
    for model_dir in obliterated_dir.iterdir():
        if model_dir.is_dir():
            size = sum(f.stat().st_size for f in model_dir.rglob("*.safetensors")) / 1e9
            models.append((model_dir.name, size))
    
    for i, (name, size) in enumerate(sorted(models), 1):
        output.append(f"  {i}. {name} ({size:.1f} GB)")
    
    output.append("\n" + "="*50)
    output.append("Type /use <model_name> to switch")
    
    return "\n".join(output)
