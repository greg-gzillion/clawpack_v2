"""Route registry - collects all routes"""
from .math_routes import MathRoutes
from .web_routes import WebRoutes
from .translation_routes import TranslationRoutes
from .legal_routes import LegalRoutes
from .medical_routes import MedicalRoutes
from .code_routes import CodeRoutes
from .data_routes import DataRoutes
from .document_routes import DocumentRoutes
from .language_routes import LanguageRoutes
from .blockchain_routes import BlockchainRoutes
from .fork_routes import ForkRoutes
from .voice_routes import VoiceRoutes

class RouteRegistry:
    def __init__(self):
        self.routes = [
            MathRoutes,
            WebRoutes,
            TranslationRoutes,
            LegalRoutes,
            MedicalRoutes,
            CodeRoutes,
            DataRoutes,
            DocumentRoutes,
            LanguageRoutes,
            BlockchainRoutes,
            ForkRoutes,
            VoiceRoutes
        ]
        self.command_map = {}
        self._build_map()
    
    def _build_map(self):
        for route in self.routes:
            for cmd in route.commands:
                self.command_map[cmd] = route.agent
    
    def get_agent(self, command: str) -> str:
        """Get agent name for a command"""
        return self.command_map.get(command, 'mathematicaclaw')
    
    def get_all_help(self) -> str:
        """Get help from all routes"""
        help_text = ""
        for route in self.routes:
            help_text += route.get_help()
        return help_text

_registry = None

def get_registry():
    global _registry
    if _registry is None:
        _registry = RouteRegistry()
    return _registry
