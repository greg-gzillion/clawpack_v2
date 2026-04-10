"""Mathematicaclaw Math Engine - Pure sympy/numpy/matplotlib functions"""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

class MathEngine:
    """Pure math operations - no CLI, no state"""
    
    def __init__(self):
        self.x, self.y, self.z = sp.symbols('x y z')
    
    def solve_equation(self, equation: str) -> dict:
        """Solve an equation (handles both 'expr = expr' and just 'expr')"""
        try:
            if '=' in equation:
                left, right = equation.split('=')
                eq = sp.Eq(sp.sympify(left.strip()), sp.sympify(right.strip()))
            else:
                eq = sp.sympify(equation)
            solutions = sp.solve(eq)
            return {"success": True, "solutions": [str(s) for s in solutions]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def derivative(self, expression: str, variable: str = 'x') -> dict:
        """Compute derivative"""
        try:
            expr = sp.sympify(expression)
            var = sp.Symbol(variable)
            result = sp.diff(expr, var)
            return {"success": True, "result": str(result)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def integral(self, expression: str, variable: str = 'x', a=None, b=None) -> dict:
        """Compute integral (definite or indefinite)"""
        try:
            expr = sp.sympify(expression)
            var = sp.Symbol(variable)
            if a is not None and b is not None:
                result = sp.integrate(expr, (var, a, b))
            else:
                result = sp.integrate(expr, var)
            return {"success": True, "result": str(result)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def limit(self, expression: str, variable: str, point: float) -> dict:
        """Compute limit"""
        try:
            expr = sp.sympify(expression)
            var = sp.Symbol(variable)
            result = sp.limit(expr, var, point)
            return {"success": True, "result": str(result)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def simplify(self, expression: str) -> dict:
        """Simplify expression"""
        try:
            expr = sp.sympify(expression)
            result = sp.simplify(expr)
            return {"success": True, "result": str(result)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def factor(self, expression: str) -> dict:
        """Factor expression"""
        try:
            expr = sp.sympify(expression)
            result = sp.factor(expr)
            return {"success": True, "result": str(result)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def expand(self, expression: str) -> dict:
        """Expand expression"""
        try:
            expr = sp.sympify(expression)
            result = sp.expand(expr)
            return {"success": True, "result": str(result)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def plot(self, expression: str, x_min=-10, x_max=10, output_file=None) -> dict:
        """Plot function using matplotlib"""
        try:
            expr = sp.sympify(expression)
            f = sp.lambdify(self.x, expr, modules=['numpy'])
            
            x_vals = np.linspace(x_min, x_max, 1000)
            y_vals = f(x_vals)
            
            plt.figure(figsize=(10, 6))
            plt.plot(x_vals, y_vals)
            plt.grid(True)
            plt.title(f"f(x) = {expression}")
            plt.xlabel('x')
            plt.ylabel('f(x)')
            
            if output_file:
                plt.savefig(output_file)
                plt.close()
                return {"success": True, "file": output_file}
            else:
                export_dir = Path("exports")
                export_dir.mkdir(exist_ok=True)
                filename = export_dir / f"plot_{abs(hash(expression))}.png"
                plt.savefig(filename)
                plt.close()
                return {"success": True, "file": str(filename)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def solve(self, equation: str) -> dict:
        """Alias for solve_equation for compatibility"""
        return self.solve_equation(equation)

    def evaluate_arithmetic(self, expression: str) -> dict:
        """Handle simple arithmetic without variables"""
        try:
            # Import sympy for evaluation
            result = sp.sympify(expression)
            return {"success": True, "solutions": [str(result)]}
        except Exception as e:
            return {"success": False, "error": str(e)}
