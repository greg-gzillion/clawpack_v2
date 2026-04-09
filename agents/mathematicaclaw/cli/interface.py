"""Mathematicaclaw CLI Interface"""

import os
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.agent import MathematicaclawAgent

class MathematicaclawCLI:
    def __init__(self):
        self.agent = MathematicaclawAgent()
    
    def run(self):
        self._show_header()
        while True:
            try:
                cmd = input("\n📐 Math > ").strip()
                if not cmd:
                    continue
                
                if cmd == "/quit":
                    print("Goodbye!")
                    break
                elif cmd == "/clear":
                    os.system('cls')
                    self._show_header()
                elif cmd == "/help":
                    self._show_help()
                elif cmd == "/stats":
                    self._show_stats()
                elif cmd.startswith("/solve"):
                    self._solve(cmd[6:].strip())
                elif cmd.startswith("/derivative"):
                    self._derivative(cmd[11:].strip())
                elif cmd.startswith("/integral"):
                    self._integral(cmd[9:].strip())
                elif cmd.startswith("/simplify"):
                    self._simplify(cmd[9:].strip())
                elif cmd.startswith("/factor"):
                    self._factor(cmd[7:].strip())
                elif cmd.startswith("/expand"):
                    self._expand(cmd[7:].strip())
                elif cmd.startswith("/evaluate"):
                    self._evaluate(cmd[9:].strip())
                elif cmd.startswith("/stats"):
                    self._statistics(cmd[6:].strip())
                elif cmd.startswith("/matrix"):
                    self._matrix(cmd[7:].strip())
                elif cmd.startswith("/limit"):
                    self._limit(cmd[6:].strip())
                elif cmd.startswith("/series"):
                    self._series(cmd[7:].strip())
                elif cmd.startswith("/system"):
                    self._system(cmd[7:].strip())
                else:
                    print("Unknown command. Type /help")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def _show_header(self):
        print("\n" + "="*60)
        print("MATHEMATICACLAW - Mathematical Computation Agent".center(60))
        print("="*60)
        print("Powered by SymPy & NumPy".center(60))
        print("="*60)
        self._show_help()
    
    def _show_help(self):
        print("""
📐 COMMANDS:
  /solve <equation>            - Solve equation (e.g., /solve x**2 - 4)
  /derivative <expr> [var]      - Derivative (e.g., /derivative x**2)
  /integral <expr> [var]        - Integral (e.g., /integral x**2)
  /simplify <expr>              - Simplify expression
  /factor <expr>                - Factor expression
  /expand <expr>                - Expand expression
  /evaluate <expr> <var=val>    - Evaluate with values
  /matrix <op> <data>           - Matrix operations
  /limit <expr> <var> <point>   - Calculate limit
  /series <expr> <var>          - Taylor series
  /system <eq1> <eq2> ...       - Solve system
  /stats <data>                 - Basic statistics
  /stats                        - Session statistics
  /help                         - Show help
  /quit                         - Exit

EXAMPLES:
  /solve x**2 - 4
  /derivative sin(x)
  /integral x**2
  /simplify (x**2 + 2*x + 1)/(x + 1)
  /evaluate x**2 + y x=2 y=3
""")
    
    def _show_stats(self):
        stats = self.agent.get_stats()
        print(f"\n📊 Session Statistics:")
        print(f"   Total queries: {stats['total_queries']}")
        if stats['operations']:
            print("   Operations:")
            for op, count in stats['operations'].items():
                print(f"     {op}: {count}")
    
    def _solve(self, arg):
        parts = arg.split()
        if len(parts) >= 1:
            expr = parts[0]
            var = parts[1] if len(parts) > 1 else 'x'
            result = self.agent.solve(expr, var)
            self._display_result(result)
        else:
            print("Usage: /solve <equation> [variable]")
    
    def _derivative(self, arg):
        parts = arg.split()
        if len(parts) >= 1:
            expr = parts[0]
            var = parts[1] if len(parts) > 1 else 'x'
            order = int(parts[2]) if len(parts) > 2 else 1
            result = self.agent.derivative(expr, var, order)
            self._display_result(result)
        else:
            print("Usage: /derivative <expression> [variable] [order]")
    
    def _integral(self, arg):
        parts = arg.split()
        if len(parts) >= 1:
            expr = parts[0]
            var = parts[1] if len(parts) > 1 else 'x'
            result = self.agent.integral(expr, var)
            self._display_result(result)
        else:
            print("Usage: /integral <expression> [variable]")
    
    def _simplify(self, arg):
        if arg:
            result = self.agent.simplify(arg)
            self._display_result(result)
        else:
            print("Usage: /simplify <expression>")
    
    def _factor(self, arg):
        if arg:
            result = self.agent.factor(arg)
            self._display_result(result)
        else:
            print("Usage: /factor <expression>")
    
    def _expand(self, arg):
        if arg:
            result = self.agent.expand(arg)
            self._display_result(result)
        else:
            print("Usage: /expand <expression>")
    
    def _evaluate(self, arg):
        parts = arg.split()
        if len(parts) >= 1:
            expr = parts[0]
            values = {}
            for p in parts[1:]:
                if '=' in p:
                    k, v = p.split('=')
                    values[k] = float(v)
            result = self.agent.evaluate(expr, values)
            self._display_result(result)
        else:
            print("Usage: /evaluate <expression> <var=value> ...")
    
    def _statistics(self, arg):
        if arg:
            try:
                data = [float(x) for x in arg.split()]
                result = self.agent.stats(data)
                self._display_result(result)
            except:
                print("Usage: /stats <num1> <num2> ...")
        else:
            self._show_stats()
    
    def _matrix(self, arg):
        print("Matrix operations: /matrix det [[1,2],[3,4]]")
        print("Operations: det, inv, eigenvals, transpose, rank")
    
    def _limit(self, arg):
        parts = arg.split()
        if len(parts) >= 3:
            expr, var, point = parts[0], parts[1], float(parts[2])
            result = self.agent.limit(expr, var, point)
            self._display_result(result)
        else:
            print("Usage: /limit <expression> <variable> <point>")
    
    def _series(self, arg):
        parts = arg.split()
        if len(parts) >= 2:
            expr, var = parts[0], parts[1]
            point = float(parts[2]) if len(parts) > 2 else 0
            order = int(parts[3]) if len(parts) > 3 else 6
            result = self.agent.series(expr, var, point, order)
            self._display_result(result)
        else:
            print("Usage: /series <expression> <variable> [point] [order]")
    
    def _system(self, arg):
        print("System solver: /system eq1 eq2 ... --vars x y")
    
    def _display_result(self, result: dict):
        if result.get("success"):
            print(f"\n✅ Success!")
            for key, value in result.items():
                if key not in ["success", "method", "latex"]:
                    print(f"   {key}: {value}")
            if "latex" in result:
                print(f"   LaTeX: {result['latex']}")
        else:
            print(f"\n❌ Error: {result.get('error', 'Unknown error')}")

