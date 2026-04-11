#!/usr/bin/env python3
"""drawclaw - Casual Drawing Agent"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.base_agent import BaseAgent
from .core.agent import drawclawCore

class drawclawAgent(BaseAgent):
    """Casual/freeform drawing agent"""
    
    def __init__(self):
        super().__init__("drawclaw")
        self.core = drawclawCore()
    
    def handle(self, query: str) -> str:
        """Handle drawing queries"""
        self.track_interaction()
        return self.core.process(query)

def main():
    agent = drawclawAgent()
    
    if len(sys.argv) > 1:
        cmd = ' '.join(sys.argv[1:])
        print(agent.handle(cmd))
        return
    
    if not sys.stdin.isatty():
        for line in sys.stdin:
            cmd = line.strip()
            if cmd and cmd != "/quit":
                print(agent.handle(cmd))
        return
    
    print("\n🎨 DRAWCLAW - Casual Drawing Agent")
    print("Commands: sketch, doodle, paint, illustrate, cartoon, meme")
    print("Type /help for more, /quit to exit")
    
    while True:
        try:
            cmd = input("\n🎨 > ").strip()
            if cmd == "/quit":
                break
            if cmd == "/help":
                print("""
🎨 DRAWCLAW (Casual):
  sketch <desc>      - Quick pencil sketch
  doodle <desc>      - Fun doodle
  paint <desc>       - Digital painting
  illustrate <scene> - Detailed illustration
  cartoon <char>     - Cartoon character
  meme <concept>     - Meme image
  /stats             - Show statistics
  /quit              - Exit
""")
            elif cmd == "/stats":
                stats = self.get_stats()
                print(f"📊 Interactions: {stats['interactions']}")
            elif cmd:
                print(agent.handle(cmd))
        except (KeyboardInterrupt, EOFError):
            break

if __name__ == "__main__":
    main()
