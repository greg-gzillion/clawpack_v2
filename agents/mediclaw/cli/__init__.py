"""Command Line Interface"""

from core.engine import MedicalEngine
from commands import CommandRegistry
from providers import ProviderRegistry

class CLI:
    def __init__(self):
        self.engine = MedicalEngine()
        self.commands = CommandRegistry()
        self.providers = ProviderRegistry()
    
    def start(self):
        print("\n" + "="*70)
        print("🏥 MEDICLAW - Medical Research System")
        print("="*70)
        print(f"🔌 Providers: {', '.join(self.providers.get_available())}")
        print(f"📚 Sources: {len(self.engine.list_sources())}")
        print("\nCOMMANDS:")
        print("  /research <topic>     - Medical research")
        print("  /diagnose <symptoms>  - Differential diagnosis")
        print("  /treatment <condition>- Treatment guidelines")
        print("  /sources              - List sources")
        print("  /stats                - System status")
        print("  /quit                 - Exit")
        print("="*70)
        
        while True:
            try:
                cmd = input("\n🔬 mediclaw> ").strip()
                if not cmd:
                    continue
                
                if cmd == "/quit":
                    print("Goodbye!")
                    break
                
                parts = cmd.split(" ", 1)
                cmd_name = parts[0]
                args = parts[1] if len(parts) > 1 else ""
                
                command = self.commands.get(cmd_name)
                if command:
                    result = command.execute(args, self.engine)
                    print(result)
                else:
                    print(f"Unknown: {cmd_name}")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
