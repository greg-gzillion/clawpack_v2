"""LawClaw Commands - Dynamic command loading"""
import os
import sys
from pathlib import Path

COMMAND_REGISTRY = {}

def load_all_commands():
    """Dynamically load all command modules"""
    global COMMAND_REGISTRY
    commands_dir = Path(__file__).parent
    
    loaded_count = 0
    for file in commands_dir.glob("*.py"):
        if file.name.startswith("_"):
            continue
        
        module_name = file.stem
        try:
            # Import the module
            spec = importlib.util.spec_from_file_location(module_name, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Get the command name and run function
            if hasattr(module, 'name') and hasattr(module, 'run'):
                cmd_name = module.name
                COMMAND_REGISTRY[cmd_name] = module.run
                print(f"  [OK] Loaded: {cmd_name}")
                loaded_count += 1
                
        except Exception as e:
            print(f"  [ERROR] Loading {module_name}: {e}")
    
    print(f"\n[OK] Total commands loaded: {loaded_count}")
    return COMMAND_REGISTRY

def get_command_help():
    """Get help text for all commands"""
    help_lines = ["LawClaw Commands:", "=" * 50]
    for cmd_name in sorted(COMMAND_REGISTRY.keys()):
        help_lines.append(f"  {cmd_name}")
    return "\n".join(help_lines)

# Auto-load on import
import importlib
COMMAND_REGISTRY = load_all_commands()
