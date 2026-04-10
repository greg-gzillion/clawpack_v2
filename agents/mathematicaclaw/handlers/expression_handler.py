"""Handles direct mathematical expressions"""
import sympy as sp
from typing import Optional

class ExpressionHandler:
    """Evaluates raw mathematical expressions"""
    
    def evaluate(self, expression: str) -> Optional[str]:
        """Try to evaluate as a math expression"""
        try:
            expr = sp.sympify(expression)
            result = sp.simplify(expr)
            return f"Result: {result}"
        except:
            return None
