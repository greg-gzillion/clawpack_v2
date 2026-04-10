"""Algebra operations"""
import sympy as sp

class AlgebraOps:
    @staticmethod
    def solve(args: str) -> str:
        try:
            if '=' in args:
                left, right = args.split('=')
                eq = sp.Eq(sp.sympify(left.strip()), sp.sympify(right.strip()))
            else:
                eq = sp.sympify(args)
            
            solutions = sp.solve(eq)
            if solutions:
                return f"Solutions: {', '.join(str(s) for s in solutions)}"
            return "No solutions"
        except Exception as e:
            return f"Error: {e}"
    
    @staticmethod
    def simplify(args: str) -> str:
        try:
            expr = sp.sympify(args)
            return f"Simplified: {sp.simplify(expr)}"
        except Exception as e:
            return f"Error: {e}"
