#!/usr/bin/env python3
"""MathematicaClaw - Complete Mathematics Assistant with Chronicle Learning"""

import sys
from pathlib import Path

# Import from our math commands module
sys.path.insert(0, str(Path(__file__).parent))
from commands.math import solve, explain, search, stats

class MathematicaClaw:
    def __init__(self):
        print("🧮 MathematicaClaw Ready", file=sys.stderr)
    
    def solve_problem(self, problem):
        """Solve a mathematics problem"""
        print(f"\n🔢 Solving: {problem}\n")
        result = solve(problem)
        print(result)
        return result
    
    def explain_concept(self, concept):
        """Explain a mathematical concept"""
        print(f"\n📚 Explaining: {concept}\n")
        result = explain(concept)
        print(result)
        return result
    
    def search_resources(self, topic):
        """Search chronicle for mathematics resources"""
        print(f"\n🔍 Searching chronicle for: {topic}\n")
        result = search(topic)
        print(result)
        return result
    
    def show_stats(self):
        """Show chronicle statistics"""
        print("\n📊 Chronicle Index Statistics\n")
        result = stats()
        print(result)
        return result
    
    def plot_function(self, expression):
        """Plot a mathematical function"""
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            import sympy as sp
            
            x = sp.Symbol('x')
            expr = sp.sympify(expression)
            f = sp.lambdify(x, expr, modules=['numpy'])
            x_vals = np.linspace(-10, 10, 1000)
            y_vals = f(x_vals)
            
            plt.figure(figsize=(10, 6))
            plt.plot(x_vals, y_vals, 'b-', linewidth=2)
            plt.grid(True, alpha=0.3)
            plt.title(f'f(x) = {expression}')
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.axhline(y=0, color='k', linewidth=0.5)
            plt.axvline(x=0, color='k', linewidth=0.5)
            plt.show()
            
            return f"✅ Plot of f(x) = {expression} displayed"
        except Exception as e:
            return f"❌ Plot error: {e}"
    
    def add_numbers(self, a, b):
        """Simple addition"""
        try:
            result = float(a) + float(b)
            return f"{a} + {b} = {result}"
        except:
            return f"Invalid numbers: {a}, {b}"
    
    def process(self, command, *args):
        """Process commands"""
        if command == "solve" and args:
            return self.solve_problem(' '.join(args))
        elif command == "explain" and args:
            return self.explain_concept(' '.join(args))
        elif command == "search" and args:
            return self.search_resources(' '.join(args))
        elif command == "stats":
            return self.show_stats()
        elif command == "plot" and args:
            return self.plot_function(' '.join(args))
        elif command == "add" and len(args) >= 2:
            return self.add_numbers(args[0], args[1])
        else:
            return self.help()
    
    def help(self):
        return """
╔══════════════════════════════════════════════════════════════════╗
║              MATHEMATICACLAW - Mathematics Assistant             ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  COMMANDS:                                                       ║
║    solve <problem>     - Solve a math problem                   ║
║    explain <concept>   - Explain a concept                      ║
║    search <topic>      - Search chronicle for resources         ║
║    plot <expression>   - Plot f(x) function                     ║
║    add <a> <b>         - Add two numbers                        ║
║    stats               - Show chronicle statistics              ║
║                                                                  ║
║  EXAMPLES:                                                       ║
║    python mathematicaclaw.py solve "2x + 5 = 15"                ║
║    python mathematicaclaw.py explain "Pythagorean theorem"      ║
║    python mathematicaclaw.py search "calculus"                  ║
║    python mathematicaclaw.py plot "x**2"                        ║
║    python mathematicaclaw.py stats                              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝"""
    
    def interactive(self):
        """Interactive mode"""
        print(self.help())
        while True:
            try:
                cmd = input("\n🧮 math> ").strip()
                if not cmd:
                    continue
                if cmd.lower() in ['quit', 'exit']:
                    print("Goodbye!")
                    break
                
                parts = cmd.split(maxsplit=1)
                if len(parts) == 1:
                    if parts[0] == "stats":
                        print(self.show_stats())
                    else:
                        print("Unknown command")
                else:
                    result = self.process(parts[0], parts[1])
                    if result:
                        print(result)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break

def main():
    agent = MathematicaClaw()
    if len(sys.argv) < 2:
        print(agent.help())
        return
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    result = agent.process(command, *args)
    if result:
        print(result)

if __name__ == "__main__":
    main()
