#!/usr/bin/env python3
"""MathematicaClaw - Mathematics and Visualization Agent"""

import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class MathematicaClawAgent:
    def __init__(self):
        self.name = "mathematicaclaw"
        self.llm = None
        self._init_llm()
        self._init_visualizer()
    
    def _init_llm(self):
        try:
            from core.llm_manager import get_llm_manager
            self.llm = get_llm_manager()
        except:
            pass
    
    def _init_visualizer(self):
        try:
            from agents.mathematicaclaw.ai_visualizer import ai_visualizer
            self.visualizer = ai_visualizer
        except:
            self.visualizer = None
    
    def handle(self, cmd: str) -> str:
        cmd = cmd.strip()
        
        if cmd.startswith("/visualize"):
            return self.visualize(cmd[10:].strip())
        elif cmd.startswith("/solve"):
            return self.solve(cmd[6:].strip())
        elif cmd.startswith("/plot"):
            return self.plot(cmd[5:].strip())
        else:
            return self._help()
    
    def visualize(self, request: str) -> str:
        if not request:
            return "Usage: /visualize <description>\nExample: /visualize show me a wave"
        
        if self.visualizer:
            return self.visualizer.visualize(request)
        return "Visualizer not available. Please install matplotlib and numpy."
    
    def solve(self, equation: str) -> str:
        return f"Solving: {equation}\n(LLM integration coming soon)"
    
    def plot(self, function: str) -> str:
        return f"Plotting: {function}\n(Use /visualize for AI-powered plotting)"
    
    def _help(self):
        return """
MATHEMATICACLAW - Mathematics and Visualization

COMMANDS:
  /visualize <description>  - AI-powered math visualization
  /solve <equation>         - Solve equations
  /plot <function>          - Plot functions

EXAMPLES:
  /visualize show me a wave
  /visualize show me a 3D mountain
  /visualize show me a fractal
"""

def main():
    agent = MathematicaClawAgent()
    if len(sys.argv) > 1:
        print(agent.handle(' '.join(sys.argv[1:])))
    else:
        print(agent._help())

if __name__ == "__main__":
    main()
