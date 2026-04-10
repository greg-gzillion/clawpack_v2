"""Calculus operations"""
import sympy as sp

class CalculusOps:
    @staticmethod
    def derivative(args: str) -> str:
        try:
            expr = sp.sympify(args)
            return f"Derivative: {sp.diff(expr)}"
        except Exception as e:
            return f"Error: {e}"
    
    @staticmethod
    def integral(args: str) -> str:
        try:
            expr = sp.sympify(args)
            return f"Integral: {sp.integrate(expr)} + C"
        except Exception as e:
            return f"Error: {e}"
