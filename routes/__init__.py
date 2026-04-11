"""Routes module - auto-discovered by clawpack.py"""
from .math_routes import MathRoutes
from .web_routes import WebRoutes
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

__all__ = [
    'MathRoutes', 'WebRoutes', 'TranslationRoutes', 'LawclawRoutes',
    'MedicalRoutes', 'CodeRoutes', 'DataRoutes', 'DocumentRoutes',
    'LanguageRoutes', 'BlockchainRoutes', 'ForkRoutes', 'VoiceRoutes',
    'LiberateclawRoutes'
]
