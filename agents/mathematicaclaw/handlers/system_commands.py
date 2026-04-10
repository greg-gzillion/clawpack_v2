"""System commands for mathematicaclaw"""
from typing import Dict, Callable

class SystemCommands:
    """System-level commands"""
    
    @staticmethod
    def get_commands() -> Dict[str, Callable]:
        return {
            'help': SystemCommands._help,
            'test': SystemCommands._test,
            'quit': SystemCommands._quit,
        }
    
    @staticmethod
    def _help(args: str = None) -> str:
        return "Type 'help' for command list"
    
    @staticmethod
    def _test(args: str = None) -> str:
        return "✅ Mathematicaclaw is working!"
    
    @staticmethod
    def _quit(args: str = None) -> str:
        return "QUIT"
