"""Sources Command"""

from commands.base import Command

class SourcesCommand(Command):
    def name(self) -> str:
        return "/sources"
    
    def execute(self, args: str, engine) -> str:
        sources = engine.list_sources()
        output = f"\n📚 Medical Sources ({len(sources)}):\n"
        for i, s in enumerate(sources, 1):
            output += f"   {i:2}. {s}\n"
        if len(sources) > 30:
            output += f"   ... and {len(sources)-30} more"
        return output
