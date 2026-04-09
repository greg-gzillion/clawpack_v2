"""Stats Command"""

from commands.base import Command
from providers import ProviderRegistry

class StatsCommand(Command):
    def name(self) -> str:
        return "/stats"
    
    def execute(self, args: str, engine) -> str:
        providers = ProviderRegistry()
        available = providers.get_available()
        return f"\n📊 Available Providers: {', '.join(available)}\n   Sources: {len(engine.list_sources())}"
