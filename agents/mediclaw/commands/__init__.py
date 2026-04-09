"""Command Registry"""

from pathlib import Path
import sys
from .base import Command

class CommandRegistry:
    def __init__(self):
        self.commands = {}
        self._load()
    
    def _load(self):
        commands_dir = Path(__file__).parent
        for py_file in commands_dir.glob("*.py"):
            if py_file.name in ["base.py", "__init__.py"]:
                continue
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location(
                    f"commands.{py_file.stem}", py_file
                )
                module = importlib.util.module_from_spec(spec)
                sys.modules[f"commands.{py_file.stem}"] = module
                spec.loader.exec_module(module)
                
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, Command) and attr != Command:
                        cmd = attr()
                        self.commands[cmd.name()] = cmd
            except Exception as e:
                print(f"Error loading {py_file.name}: {e}")
    
    def get(self, name: str):
        return self.commands.get(name)
