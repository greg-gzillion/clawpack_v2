"""LLMClaw Command Registry"""
import importlib
from pathlib import Path

COMMAND_REGISTRY = {}

def load_all_commands():
    commands_dir = Path(__file__).parent
    loaded = 0
    
    for py_file in commands_dir.glob("*.py"):
        if py_file.name == "__init__.py":
            continue
        
        try:
            module = importlib.import_module(f"commands.{py_file.stem}")
            if hasattr(module, 'name') and hasattr(module, 'run'):
                COMMAND_REGISTRY[module.name] = module.run
                loaded += 1
        except Exception as e:
            print(f"  ❌ Error loading {py_file.name}: {e}")
    
    return COMMAND_REGISTRY

load_all_commands()
