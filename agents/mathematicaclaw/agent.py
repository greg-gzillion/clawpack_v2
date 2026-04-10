#!/usr/bin/env python3
"""Mathematicaclaw - Math Agent"""
import sys
from pathlib import Path

# Add parent to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.base_agent import BaseAgent

class MathematicaclawAgent(BaseAgent):
    """Math agent with plotting capabilities"""
    
    def __init__(self):
        super().__init__("mathematicaclaw")
    
    def handle(self, query: str) -> str:
        """Handle math command"""
        return self._run_command(query)
    
    def _run_command(self, cmd: str) -> str:
        parts = cmd.strip().split(maxsplit=1)
        if not parts:
            return self._help()
        
        cmd_name = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd_name == "add":
            try:
                nums = [float(x) for x in args.split()]
                return f"Sum: {sum(nums)}"
            except:
                return "Usage: add 2 3 4"
        
        elif cmd_name == "plot":
            try:
                import matplotlib.pyplot as plt
                import numpy as np
                import sympy as sp
                x = sp.Symbol('x')
                expr = sp.sympify(args)
                f = sp.lambdify(x, expr, modules=['numpy'])
                x_vals = np.linspace(-10, 10, 1000)
                y_vals = f(x_vals)
                plt.figure(figsize=(10, 6))
                plt.plot(x_vals, y_vals, 'b-', linewidth=2)
                plt.grid(True, alpha=0.3)
                plt.title(f'f(x) = {args}')
                plt.xlabel('x')
                plt.ylabel('f(x)')
                plt.axhline(y=0, color='k', linewidth=0.5)
                plt.axvline(x=0, color='k', linewidth=0.5)
                plt.show(block=True)
                plt.close()
                return f"✅ Plot of '{args}' displayed"
            except Exception as e:
                return f"Plot error: {e}"
        
        elif cmd_name == "solve":
            try:
                import sympy as sp
                if '=' in args:
                    left, right = args.split('=')
                    eq = sp.Eq(sp.sympify(left.strip()), sp.sympify(right.strip()))
                else:
                    eq = sp.sympify(args)
                solutions = sp.solve(eq)
                return f"Solutions: {', '.join(str(s) for s in solutions)}"
            except Exception as e:
                return f"Error: {e}"
        
        elif cmd_name == "derivative":
            try:
                import sympy as sp
                expr = sp.sympify(args)
                return f"Derivative: {sp.diff(expr)}"
            except:
                return "Usage: derivative x**3"
        
        elif cmd_name == "integral":
            try:
                import sympy as sp
                expr = sp.sympify(args)
                return f"Integral: {sp.integrate(expr)} + C"
            except:
                return "Usage: integral x**2"
        
        elif cmd_name in ["help", "/help"]:
            return self._help()
        
        elif cmd_name in ["quit", "exit", "/quit"]:
            return "QUIT"
        
        else:
            return f"Unknown: {cmd_name}. Type 'help' for commands."
    
    def _help(self) -> str:
        return """
Commands:
  add 2 3 4        - Add numbers
  solve x**2 = 16  - Solve equation
  plot x**2        - Plot function (opens window)
  derivative x**3  - Calculate derivative
  integral x**2    - Calculate integral
  help             - Show this
  quit             - Exit
"""

    def run_cli(self):
        """Run interactive CLI"""
        print("Mathematicaclaw - Math Agent")
        print("Type 'help' for commands, 'quit' to exit\n")
        
        while True:
            try:
                cmd = input("math> ").strip()
                if not cmd:
                    continue
                result = self.handle(cmd)
                print(result)
                if result == "QUIT":
                    break
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break

if __name__ == "__main__":
    agent = MathematicaclawAgent()
    agent.run_cli()
