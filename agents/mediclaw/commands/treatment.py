"""Treatment Command"""

from commands.base import Command

class TreatmentCommand(Command):
    def name(self) -> str:
        return "/treatment"
    
    def execute(self, args: str, engine) -> str:
        if not args:
            return "Usage: /treatment <condition>"
        return engine.treatment(args)
