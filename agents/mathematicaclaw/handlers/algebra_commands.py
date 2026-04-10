"""Algebra operations"""
import sympy as sp
from typing import Dict, Callable

class AlgebraCommands:
    """All algebra-related commands"""
    
    @staticmethod
    def get_commands() -> Dict[str, Callable]:
        return {
            'solve': AlgebraCommands._solve,
            'simplify': AlgebraCommands._simplify,
            'factor': AlgebraCommands._factor,
            'expand': AlgebraCommands._expand,
            'evaluate': AlgebraCommands._evaluate,
            'eval': AlgebraCommands._evaluate,
        }
    
    @staticmethod
    def _solve(args: str) -> str:
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
            return f"Error: {e}"
    
    @staticmethod
    def _simplify(args: str) -> str:
        try:
            expr = sp.sympify(args)
            return f"Simplified: {sp.simplify(expr)}"
        except Exception as e:
            return f"Error: {e}"
    
    @staticmethod
    def _factor(args: str) -> str:
        try:
            expr = sp.sympify(args)
            return f"Factored: {sp.factor(expr)}"
        except Exception as e:
            return f"Error: {e}"
    
    @staticmethod
    def _expand(args: str) -> str:
        try:
            expr = sp.sympify(args)
            return f"Expanded: {sp.expand(expr)}"
        except Exception as e:
            return f"Error: {e}"
    
    @staticmethod
    def _evaluate(args: str) -> str:
        try:
            if 'at' in args:
                expr_str, point_str = args.split('at')
                expr = sp.sympify(expr_str.strip())
                var, val = point_str.split('=')
                var_sym = sp.Symbol(var.strip())
                val = float(val.strip())
                result = expr.subs(var_sym, val)
                return f"Result: {result}"
            return "Usage: evaluate x**2 at x=3"
        except Exception as e:
            return f"Error: {e}"
    
    @staticmethod
    def get_help() -> str:
        return """
📊 ALGEBRA:
  solve x**2 = 16     - Solve equations
  simplify (x**2+2x+1)/(x+1) - Simplify
  factor x**2+2x+1    - Factor
  expand (x+1)**2     - Expand
  evaluate x**2 at x=3 - Evaluate

"""
