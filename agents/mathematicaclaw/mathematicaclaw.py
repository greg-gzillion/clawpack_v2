#!/usr/bin/env python3
"""MathematicaClaw - Mathematics and Visualization"""

import sys
from pathlib import Path

# A2A Collaboration Layer
try:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from agents.shared.a2a_client import A2AClient
    a2a_client = A2AClient()
except Exception as e:
    a2a_client = None
    print(f"⚠ A2A unavailable: {e}")


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class MathematicaClawAgent:
    def __init__(self):
        self.name = "mathematicaclaw"
        self.visualizer = None
        self._init_visualizer()
    
    def _init_visualizer(self):
        try:
            from agents.mathematicaclaw.ai_visualizer import ai_visualizer
            self.visualizer = ai_visualizer
        except Exception as e:
            print(f"âš ï¸ Visualizer error: {e}", file=sys.stderr)
    
    def handle(self, cmd: str) -> str:
        cmd = cmd.strip()
        
        if cmd.startswith("/visualize") or cmd.startswith("/math"):
            # Remove the command prefix
            rest = cmd[10:].strip() if cmd.startswith("/visualize") else cmd[5:].strip()
            return self.visualize(rest)
        else:
            return self._help()
    
    def visualize(self, request: str) -> str:
        if not request:
            return "Usage: /visualize <description>\nExample: /visualize sine wave"
        
        if self.visualizer:
            return self.visualizer.visualize(request)
        return "Visualizer not available"
    
    def _help(self):
        return """
MATH CLAW - AI-Powered Math Visualization

COMMANDS:
  /visualize <desc>  - Generate AI visualization
  /math <desc>       - Same as /visualize

EXAMPLES:
  /visualize sine wave
  /visualize 3D mountain
  /visualize parabola
  /math fractal
"""

def main():
    agent = MathematicaClawAgent()
    if len(sys.argv) > 1:
        print(agent.handle(' '.join(sys.argv[1:])))
    else:
        print(agent._help())

if __name__ == "__main__":
    main()

