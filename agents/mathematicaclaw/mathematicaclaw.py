#!/usr/bin/env python3
"""Mathematicaclaw - Modular Math Agent"""
import sys
from pathlib import Path

# Add the ROOT clawpack_v2 to path for shared modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.base_agent import BaseAgent

# Import math engine from local core
sys.path.insert(0, str(Path(__file__).parent))
from core.math_engine import MathEngine

class MathematicaclawAgent(BaseAgent):
    """Math agent with sympy/numpy/matplotlib"""
    
    def __init__(self):
        super().__init__("mathematicaclaw")
        self.engine = MathEngine()
    
    def handle(self, query: str) -> str:
        """Handle math queries"""
        self.track_interaction()
        
        parts = query.split(maxsplit=1)
        if not parts:
            return self._help()
        
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""
        
        if cmd in ["solve", "/solve"]:
            result = self.engine.solve_equation(arg)
        elif cmd in ["derivative", "/derivative", "diff", "/diff"]:
            result = self.engine.derivative(arg)
        elif cmd in ["integral", "/integral", "int", "/int"]:
            result = self.engine.integral(arg)
        elif cmd in ["limit", "/limit"]:
            if "->" in arg:
                expr_part, limit_part = arg.split("->")
                var, val = limit_part.strip().split("=") if "=" in limit_part else ('x', limit_part.strip())
                result = self.engine.limit(expr_part.strip(), var.strip(), float(val))
            else:
                return "Use: limit <expr> x->a"
        elif cmd in ["simplify", "/simplify"]:
            result = self.engine.simplify(arg)
        elif cmd in ["factor", "/factor"]:
            result = self.engine.factor(arg)
        elif cmd in ["expand", "/expand"]:
            result = self.engine.expand(arg)
        elif cmd in ["plot", "/plot"]:
            result = self.engine.plot(arg)
        elif cmd in ["help", "/help"]:
            return self._help()
        elif cmd in ["stats", "/stats"]:
            return self._stats()
        else:
            result = self.engine.solve_equation(query)
        
        if result.get("success"):
            if "file" in result:
                return f"Plot saved: {result['file']}"
            elif "solutions" in result:
                return f"Solutions: {', '.join(result['solutions'])}"
            else:
                return f"{result.get('result', 'Done')}"
        else:
            return f"Error: {result.get('error', 'Unknown')}"
    
    def _help(self) -> str:
        return """
MATHEMATICACLAW COMMANDS:
  solve <equation>        - Solve equation
  derivative <expr>       - Compute derivative
  integral <expr>         - Compute integral
  limit <expr> x->a       - Compute limit
  simplify <expr>         - Simplify expression
  factor <expr>           - Factor expression
  expand <expr>           - Expand expression
  plot <expr>             - Plot function
  /stats                  - Show statistics
"""
    
    def _stats(self) -> str:
        stats = self.get_stats()
        return f"Interactions: {stats['interactions']}"

def main():
    agent = MathematicaclawAgent()
    if len(sys.argv) > 1:
        print(agent.handle(' '.join(sys.argv[1:])))
    else:
        agent.run_cli()

if __name__ == "__main__":
    main()
