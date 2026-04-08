"""Auto-discover all commands"""

import importlib.util
from pathlib import Path

def get_all_commands():
    commands = {}
    cmds_path = Path(__file__).parent
    
    for py_file in cmds_path.glob("*.py"):
        if py_file.name.startswith("__"):
            continue
        try:
            spec = importlib.util.spec_from_file_location(py_file.stem, py_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, 'name') and hasattr(module, 'run'):
                commands[module.name] = module.run
        except:
            pass
    return commands

__all__ = ['get_all_commands']
