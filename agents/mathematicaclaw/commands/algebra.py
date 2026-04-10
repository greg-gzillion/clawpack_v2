"""Algebra commands for mathematicaclaw"""
import sympy as sp

def solve(args=None):
    """Solve equation: solve x**2 = 16"""
    if args:
        try:
            if '=' in args:
                left, right = args.split('=')
                eq = sp.Eq(sp.sympify(left.strip()), sp.sympify(right.strip()))
            else:
                eq = sp.sympify(args)
            
            solutions = sp.solve(eq)
            if solutions:
                return f"Solutions: {', '.join(str(s) for s in solutions)}"
            return "No solutions found"
        except Exception as e:
            return f"Error: {str(e)}"
    return "Usage: solve x**2 = 16"

def simplify(args=None):
    """Simplify expression: simplify (x**2 + 2*x + 1)/(x + 1)"""
    if args:
        try:
            expr = sp.sympify(args)
            result = sp.simplify(expr)
            return f"Simplified: {result}"
        except Exception as e:
            return f"Error: {str(e)}"
    return "Usage: simplify (x**2 + 2*x + 1)/(x + 1)"

def factor(args=None):
    """Factor expression: factor x**2 + 2*x + 1"""
    if args:
        try:
            expr = sp.sympify(args)
            result = sp.factor(expr)
            return f"Factored: {result}"
        except Exception as e:
            return f"Error: {str(e)}"
    return "Usage: factor x**2 + 2*x + 1"

def expand(args=None):
    """Expand expression: expand (x+1)**2"""
    if args:
        try:
            expr = sp.sympify(args)
            result = sp.expand(expr)
            return f"Expanded: {result}"
        except Exception as e:
            return f"Error: {str(e)}"
    return "Usage: expand (x+1)**2"

def evaluate(args=None):
    """Evaluate at point: evaluate x**2 at x=3"""
    if args and 'at' in args:
        try:
            expr_str, point_str = args.split('at')
            expr = sp.sympify(expr_str.strip())
            var, val = point_str.split('=')
            var_sym = sp.Symbol(var.strip())
            val = float(val.strip())
            result = expr.subs(var_sym, val)
            return f"{expr_str.strip()} at {var}={val} = {result}"
        except Exception as e:
            return f"Error: {str(e)}"
    return "Usage: evaluate x**2 at x=3"
