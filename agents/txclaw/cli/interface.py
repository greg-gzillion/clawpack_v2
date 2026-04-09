"""TXclaw CLI Interface"""

import os
import sys
from pathlib import Path

# Add the root directory to path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from core.agent import TXclawAgent
from core.commands import TXCommands
from cli.commands_list import CommandRegistry

class TXclawCLI:
    """Main CLI interface for TXclaw"""
    
    def __init__(self):
        self.agent = TXclawAgent()
        self.commands = TXCommands(self.agent)
        self.registry = CommandRegistry(self.commands)
    
    def run(self):
        """Main CLI loop"""
        self._show_header()
        
        while True:
            try:
                cmd_input = input("\n🔗 TX > ").strip()
                if not cmd_input:
                    continue
                
                # Built-in commands
                if cmd_input == "/quit":
                    print("Goodbye!")
                    break
                elif cmd_input == "/clear":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self._show_header()
                    continue
                elif cmd_input == "/sources":
                    self._show_sources()
                    continue
                elif cmd_input == "/stats":
                    self._show_stats()
                    continue
                elif cmd_input == "/help":
                    self._show_help()
                    continue
                
                # Parse command
                parts = cmd_input.split(maxsplit=1)
                cmd = parts[0].lstrip('/').lower()
                arg = parts[1] if len(parts) > 1 else ""
                
                # Execute command
                handler = self.registry.get_handler(cmd)
                if handler:
                    result = handler(arg)
                    print(f"\n{result}")
                    self.agent.add_query(cmd_input)
                else:
                    print(f"Unknown command: {cmd_input}. Type /help for available commands.")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
    
    def _show_header(self):
        """Display welcome header"""
        print("\n" + "="*70)
        print("TXCLAW - TX Blockchain Reference Agent".center(70))
        print("="*70)
        print("TX Blockchain Network".center(70))
        print("="*70)
        self._show_help()
    
    def _show_help(self):
        """Display help menu"""
        print("""
TX BLOCKCHAIN COMMANDS:
  /tx <hash>         - Analyze TX transaction
  /block <height>    - Get TX block information
  /address <addr>    - Look up TX address
  /token <id>        - Get TX token information
  /validator <addr>  - Get validator info
  /staking           - TX staking information
  /gas               - Current TX gas fees
  /mempool           - Pending TX transactions
  /contract <addr>   - Analyze TX smart contract
  /ecosystem         - TX ecosystem overview
  /gov [proposal]    - TX governance proposals
  /stats             - TX network statistics

UTILITIES:
  /sources           - List webclaw sources
  /stats             - Session statistics
  /clear             - Clear screen
  /quit              - Exit
""")
    
    def _show_sources(self):
        """Show webclaw sources"""
        sources = self.agent.webclaw_sources()
        print(f"\n📚 Webclaw Sources ({len(sources)}):")
        if sources:
            for i, s in enumerate(sources[:30], 1):
                print(f"   {i:3}. {s}")
        else:
            print("   No webclaw sources found.")
    
    def _show_stats(self):
        """Show session statistics"""
        stats = self.agent.get_stats()
        print(f"\n📊 Session Statistics:")
        print(f"   Queries: {stats['queries']}")
        print(f"   Sources: {stats['sources']}")
