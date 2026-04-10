#!/usr/bin/env python3
"""draftclaw - Modular Agent"""
import sys
from pathlib import Path

# Add agents directory to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.base_agent import BaseAgent
from .core.agent import draftclawCore

class draftclawAgent(BaseAgent):
    """Main agent class inheriting from BaseAgent"""
    
    def __init__(self):
        super().__init__("draftclaw")
        self.core = draftclawCore()
    
    def handle(self, query: str) -> str:
        """Handle incoming queries"""
        self.track_interaction()
        return self.core.process(query)

def main():
    agent = draftclawAgent()
    
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
    print(f"\n🎯 draftclaw - Ready")
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
