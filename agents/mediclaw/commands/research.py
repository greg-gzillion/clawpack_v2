"""Research Command"""

from commands.base import Command

class ResearchCommand(Command):
    def name(self) -> str:
        return "/research"
    
    def execute(self, args: str, engine) -> str:
        if not args:
            return "Usage: /research <topic>"
        return engine.research(args)
