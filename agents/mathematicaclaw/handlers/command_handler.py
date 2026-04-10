"""Command routing and execution"""
from typing import Dict, Callable, Optional
from .arithmetic_commands import ArithmeticCommands
from .algebra_commands import AlgebraCommands
from .calculus_commands import CalculusCommands
from .plot_commands import PlotCommands
from .system_commands import SystemCommands

class CommandHandler:
    """Routes and executes math commands"""
    
    def __init__(self):
        self.commands: Dict[str, Callable] = {}
        self._register_all_commands()
    
    def _register_all_commands(self):
        """Register all command modules"""
        self.commands.update(ArithmeticCommands.get_commands())
        self.commands.update(AlgebraCommands.get_commands())
        self.commands.update(CalculusCommands.get_commands())
        self.commands.update(PlotCommands.get_commands())
        self.commands.update(SystemCommands.get_commands())
    
    def handle(self, cmd: str, args: str) -> Optional[str]:
        """Execute a command if it exists"""
        if cmd in self.commands:
            return self.commands[cmd](args)
        return None
    
    def get_help(self) -> str:
        """Generate help text from all command modules"""
        help_text = """
╔══════════════════════════════════════════════════════════════╗
║                    MATHEMATICACLAW - Help                    ║
╚══════════════════════════════════════════════════════════════╝

"""
        help_text += ArithmeticCommands.get_help()
        help_text += AlgebraCommands.get_help()
        help_text += CalculusCommands.get_help()
        help_text += PlotCommands.get_help()
        help_text += "\n💡 Tip: Type any expression directly (e.g., 'x**2 + 2*x + 1')"
        return help_text
