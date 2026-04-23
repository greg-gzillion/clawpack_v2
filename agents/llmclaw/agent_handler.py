"""A2A Handler for LLMClaw - Model Management + Menu System"""
import sys
import os
import json
from pathlib import Path

LLMCLAW_DIR = Path(__file__).parent
PROJECT_ROOT = LLMCLAW_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(LLMCLAW_DIR))

def _get_working_llms():
    f = PROJECT_ROOT / "models" / "working_llms.json"
    if f.exists():
        try:
            return json.loads(f.read_text(encoding='utf-8'))
        except:
            pass
    return []

def _get_active():
    f = PROJECT_ROOT / "models" / "active_model.json"
    if f.exists():
        try:
            return json.loads(f.read_text())
        except:
            pass
    return {"model": "llama-3.1-8b-instant", "source": "groq"}

def _set_active(model_name, source):
    config = _get_active()
    config["model"] = model_name
    config["source"] = source
    if ':' in model_name:
        if 'ollama' in config.get('providers',{}):
            config['providers']['ollama']['model'] = model_name
            config['providers']['ollama']['priority'] = 1
        if 'groq' in config.get('providers',{}):
            config['providers']['groq']['priority'] = 2
    else:
        if 'groq' in config.get('providers',{}):
            config['providers']['groq']['model'] = model_name
            config['providers']['groq']['priority'] = 1
        if 'ollama' in config.get('providers',{}):
            config['providers']['ollama']['priority'] = 3
    f = PROJECT_ROOT / "models" / "active_model.json"
    f.write_text(json.dumps(config, indent=2))

def process_task(task: str, agent: str = None):
    os.chdir(str(LLMCLAW_DIR))
    task = task.strip()
    parts = task.split(maxsplit=1)
    cmd = parts[0].lower() if parts else ""
    args = parts[1] if len(parts) > 1 else ""

    try:
        if cmd == "/llm" and args:
            from commands.llm import run
            result = run(args)
        elif cmd in ("/models", "/list", "models", "list"):
            models = _get_working_llms()
            obliterated = [m for m in models if m.get('obliterated')]
            standard = [m for m in models if not m.get('obliterated')]
            active = _get_active()
            result = f"Active: {active.get('model')} ({active.get('source')})\n\n"
            result += f"🔥 OBLITERATED ({len(obliterated)}):\n"
            result += "\n".join(f"  - {m['model']} ({m.get('size','?')})" for m in obliterated)
            result += f"\n\n📦 STANDARD ({len(standard)}):\n"
            result += "\n".join(f"  - {m['model']} ({m.get('size','?')})" for m in standard)
            result += "\n\nUse /use <model_name> to switch"
        elif cmd in ("/use", "use") and args:
            _set_active(args, "ollama" if ":" in args else "groq")
            result = f"Switched to: {args}"
        elif cmd in ("/obliterated", "obliterated"):
            models = _get_working_llms()
            lib = [m for m in models if m.get('obliterated')]
            for m in lib:
                _set_active(m['model'], 'ollama')
            result = f"Obliterated models available: {len(lib)}\n" + "\n".join(m['model'] for m in lib)
        elif cmd in ("/normal", "normal"):
            models = _get_working_llms()
            std = [m for m in models if not m.get('obliterated')]
            result = f"Standard models available: {len(std)}\n" + "\n".join(m['model'] for m in std)
        elif cmd in ("/menu", "menu"):
            active = _get_active()
            models = _get_working_llms()
            result = f"🦞 LLMCLAW MODEL MANAGER\n\nActive: {active.get('model')} ({active.get('source')})\n\n"
            result += "[1] 📦 Standard Models\n[2] 🔓 Obliterated Models\n[3] 📋 List All\n"
            result += "\nCommands: /models, /use <name>, /obliterated, /normal, /menu"
        else:
            from commands.llm import run
            result = run(task)

        return {"status": "success", "result": str(result)}
    except Exception as e:
        return {"status": "error", "result": str(e)}
