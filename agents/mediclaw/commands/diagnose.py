"""Diagnose Command"""

from commands.base import Command

class DiagnoseCommand(Command):
    def name(self) -> str:
        return "/diagnose"
    
    def execute(self, args: str, engine) -> str:
        if not args:
            return "Usage: /diagnose <symptoms>"
        return engine.diagnose(args)
