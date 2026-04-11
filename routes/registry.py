"""Route registry - includes search"""
from .web_routes import WebRoutes
from .math_routes import MathRoutes
from .translation_routes import TranslationRoutes
from .lawclaw_routes import LawclawRoutes
from .medical_routes import MedicalRoutes
from .code_routes import CodeRoutes
from .data_routes import DataRoutes
from .document_routes import DocumentRoutes
from .language_routes import LanguageRoutes
from .blockchain_routes import BlockchainRoutes
from .fork_routes import ForkRoutes
from .voice_routes import VoiceRoutes
from .liberateclaw_routes import LiberateclawRoutes
from .search_routes import SearchRoutes

class RouteRegistry:
    def __init__(self):
        self.routes = [
            SearchRoutes,  # Add search first for priority
            WebRoutes, MathRoutes, TranslationRoutes, LawclawRoutes,
            MedicalRoutes, CodeRoutes, DataRoutes, DocumentRoutes,
            LanguageRoutes, BlockchainRoutes, ForkRoutes, VoiceRoutes,
            LiberateclawRoutes
        ]
        self.command_map = {}
        self._build_map()
    
    def _build_map(self):
        for route in self.routes:
            for cmd in route.commands:
                self.command_map[cmd] = getattr(route, 'agent', route.__name__.replace('Routes', '').lower())
    
    def get_agent(self, command: str) -> str:
        return self.command_map.get(command, 'mathematicaclaw')
    
    def get_all_help(self) -> str:
        help_text = ""
        for route in self.routes:
            if hasattr(route, 'get_help'):
                help_text += route.get_help()
        return help_text

_registry = None

def get_registry():
    global _registry
    if _registry is None:
        _registry = RouteRegistry()
    return _registry
