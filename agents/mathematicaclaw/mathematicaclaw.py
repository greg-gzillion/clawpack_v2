"""MathematicaClaw - Full Math Engine with SymPy, Matplotlib, and Plotly"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

class MathematicaClawAgent:
    def __init__(self):
        self.visualizer = None
        try:
            from ai_visualizer import AIVisualizer
            self.visualizer = AIVisualizer()
        except Exception:
            pass

    def handle(self, cmd: str) -> str:
        cmd = cmd.strip()
        if not cmd:
            return self._help()
        
        # /animate - Plotly interactive
        if cmd.startswith("/animate"):
            from commands.animate import run
            return run(cmd[9:].strip())
        
        # /plot - Matplotlib pop-up
        if cmd.startswith("/plot"):
            from visualization.plotter import Plotter
            return Plotter.plot_function(cmd[6:].strip())
        
        # /polar, /parametric, /contour
        if cmd.startswith("/polar"):
            from visualization.graph_builder import GraphBuilder
            return GraphBuilder.polar_plot(cmd[7:].strip())
        if cmd.startswith("/parametric"):
            from visualization.graph_builder import GraphBuilder
            parts = cmd[12:].strip().split(',')
            if len(parts) >= 2:
                return GraphBuilder.parametric_plot(parts[0].strip(), parts[1].strip())
            return "Usage: /parametric x_expr, y_expr"
        if cmd.startswith("/contour"):
            from visualization.graph_builder import GraphBuilder
            return GraphBuilder.contour_plot(cmd[9:].strip())
        
        # /derivative, /integral, /solve, /factor, /expand
        if cmd.startswith(("/derivative", "/integral", "/solve", "/factor", "/expand", "/compute")):
            return self._sympy_solve(cmd)
        
        # /visualize - AI
        if cmd.startswith("/visualize"):
            return self._visualize(cmd[11:].strip())
        
        return self._help()

    def _sympy_solve(self, cmd: str) -> str:
        try:
            from sympy import symbols, diff, integrate, solve, factor, expand, sympify
            x = symbols('x')
            expr_str = cmd.split(' ', 1)[1] if ' ' in cmd else ''
            if not expr_str:
                return "Usage: /derivative <expression>"
            expr = sympify(expr_str)
            
            if cmd.startswith('/derivative'): return f"d/dx = {diff(expr, x)}"
            if cmd.startswith('/integral'): return f"Integral = {integrate(expr, x)} + C"
            if cmd.startswith('/solve'): return f"Solutions: {solve(expr, x)}"
            if cmd.startswith('/factor'): return f"Factored: {factor(expr)}"
            if cmd.startswith('/expand'): return f"Expanded: {expand(expr)}"
            return f"Result: {sympify(cmd)}"
        except Exception as e:
            return f"Error: {str(e)[:200]}"

    def _visualize(self, text: str) -> str:
        if self.visualizer:
            return self.visualizer.visualize(text)
        return "AI visualizer not available"

    def _help(self):
        return """
MATHEMATICACLAW - Full Math Engine

PLOTS (pop-up windows):
  /plot sin(x)          Matplotlib graph
  /polar 1+cos(theta)   Polar plot
  /parametric cos(t),sin(t)  Parametric
  /contour x**2+y**2    Contour plot

ANIMATION (browser):
  /animate sin(x+t) from t=0 to 4*pi

COMPUTATION:
  /derivative x**4+3*x**2-7*x+2
  /integral 2*x**3+5*x
  /solve x**2-4
  /factor x**2-4
  /expand (x+1)**2
"""

def main():
    agent = MathematicaClawAgent()
    if len(sys.argv) > 1:
        print(agent.handle(' '.join(sys.argv[1:])))
    else:
        print(agent._help())

if __name__ == "__main__":
    main()