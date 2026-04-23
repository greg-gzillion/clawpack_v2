#!/usr/bin/env python3
"""designclaw - Creative Design Agent"""
import sys
from pathlib import Path

# Add root to path for shared
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from shared.base_agent import BaseAgent

# Use absolute import from the agent package
from agents.designclaw.core.agent import designclawCore

class designclawAgent(BaseAgent):
    def __init__(self):
        super().__init__("designclaw")
        self.core = designclawCore()
    
    def handle(self, query: str) -> str:
        self.track_interaction()
        return self.core.process(query)

def main():
    agent = designclawAgent()
    if len(sys.argv) > 1:
        print(agent.handle(' '.join(sys.argv[1:])))
    else:
        print("DESIGNCLAW ready. Type /help for commands.")
        agent.run_cli()

if __name__ == "__main__":
    main()

    def _search_chronicle(self, query):
        from shared.chronicle_helper import search_chronicle
        results = search_chronicle(query)
        if results:
            return "\n".join([f"  • {r.url}" for r in results])
        return "  No results found"
