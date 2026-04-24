"""list - List all available models"""
name = "/list"

def run(args):
    import subprocess
    import json
    from pathlib import Path
    
    models_dir = Path("C:/Users/greg/dev/clawpack_v2/models")
    config = json.load(open(models_dir / "active_model.json"))
    
    lines = []
    lines.append("\n" + "="*60)
    lines.append("  ALL MODELS")
    lines.append("="*60)
    lines.append(f"  ACTIVE: {config['model']} ({config['source']})")
    
    # Get real Ollama models
    result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
    ollama_models = []
    if result.returncode == 0:
        for line in result.stdout.strip().split('\n')[1:]:
            parts = line.split()
            if parts:
                name = parts[0]
                if len(parts) > 2:
                    size = parts[1] + ' ' + parts[2]
                else:
                    size = ''
                ollama_models.append((name, size))
    
    # Separate into categories
    obliterated = [(n, s) for n, s in ollama_models if '-liberated' in n and 'obliterated' not in n]
    stock = [(n, s) for n, s in ollama_models if '-liberated' not in n and 'hf.co' not in n]
    other = [(n, s) for n, s in ollama_models if n not in [x[0] for x in obliterated + stock]]
    
    # Cloud APIs
    lines.append("\n  CLOUD APIs:")
    lines.append(f"    claude-haiku-4-5-20251001 (anthropic){' [ACTIVE]' if config['source'] == 'anthropic' else ''}")
    lines.append(f"    llama-3.1-8b-instant (groq){' [ACTIVE]' if config['source'] == 'groq' else ''}")
    
    # Obliterated models
    lines.append(f"\n  OBLITERATED (Unrestricted - No Refusals):")
    for name, size in obliterated:
        mark = " [ACTIVE]" if config['model'] == name else ""
        lines.append(f"    {name}  {size}{mark}")
    
    # Stock Ollama models
    lines.append(f"\n  STOCK OLLAMA:")
    for name, size in stock:
        mark = " [ACTIVE]" if config['model'] == name else ""
        lines.append(f"    {name}  {size}{mark}")
    
    # Other (HF, etc)
    if other:
        lines.append(f"\n  OTHER:")
        for name, size in other:
            lines.append(f"    {name}  {size}")
    
    # Priority chain
    providers = config.get("providers", {})
    lines.append("\n" + "-"*60)
    lines.append("  FALLBACK ORDER:")
    sorted_p = sorted(providers.items(), key=lambda x: x[1].get("priority", 99))
    for i, (name, pconfig) in enumerate(sorted_p, 1):
        lines.append(f"    {i}. {name}: {pconfig.get('model', '?')}")
    
    lines.append("\n" + "="*60)
    lines.append("  /use <model> to switch")
    return "\n".join(lines)
