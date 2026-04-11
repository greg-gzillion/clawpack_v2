#!/usr/bin/env python3
"""dreamclaw - Modular Agent"""
import sys
from pathlib import Path

# Add agents directory to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.base_agent import BaseAgent
from .core.agent import dreamclawCore

class dreamclawAgent(BaseAgent):
    """Main agent class inheriting from BaseAgent"""
    
    def __init__(self):
        super().__init__("dreamclaw")
        self.core = dreamclawCore()
    
    def handle(self, query: str) -> str:
        """Handle incoming queries"""
        self.track_interaction()
        return self.core.process(query)

def main():
    agent = dreamclawAgent()
    
    # CLI mode
    if len(sys.argv) > 1:
        cmd = ' '.join(sys.argv[1:])
        print(agent.handle(cmd))
        return
    
    # Piped input
    if not sys.stdin.isatty():
        for line in sys.stdin:
            cmd = line.strip()
            if cmd and cmd != "/quit":
                print(agent.handle(cmd))
        return
    
    # Interactive mode
    print(f"\n🎯 dreamclaw - Ready")
    print("Type /help for commands, /quit to exit")
    
    while True:
        try:
            cmd = input("> ").strip()
            if cmd == "/quit":
                break
            if cmd:
                print(agent.handle(cmd))
        except (KeyboardInterrupt, EOFError):
            break

if __name__ == "__main__":
    main()

    def _search_chronicle(self, query):
        from shared.chronicle_helper import search_chronicle
        results = search_chronicle(query)
        if results:
            return "\n".join([f"  • {r.url}" for r in results[:5]])
        return "  No results found"
