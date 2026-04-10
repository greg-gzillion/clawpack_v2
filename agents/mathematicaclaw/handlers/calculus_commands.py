"""Calculus operations"""
import sympy as sp
from typing import Dict, Callable

class CalculusCommands:
    """All calculus-related commands"""
    
    @staticmethod
    def get_commands() -> Dict[str, Callable]:
        return {
            'derivative': CalculusCommands._derivative,
            'diff': CalculusCommands._derivative,
            'integral': CalculusCommands._integral,
            'int': CalculusCommands._integral,
            'limit': CalculusCommands._limit,
        }
    
    @staticmethod
    def _derivative(args: str) -> str:
        try:
            parts = args.split()
            expr_str = parts[0]
            var = parts[1] if len(parts) > 1 else 'x'
            expr = sp.sympify(expr_str)
            var_sym = sp.Symbol(var)
            return f"Derivative: {sp.diff(expr, var_sym)}"
        except Exception as e:
            return f"Error: {e}"
    
    @staticmethod
    def _integral(args: str) -> str:
        try:
            expr = sp.sympify(args)
            return f"Integral: {sp.integrate(expr)} + C"
        except Exception as e:
            return f"Error: {e}"
    
    @staticmethod
    def _limit(args: str) -> str:
        try:
            if 'as' in args:
                expr_str, limit_info = args.split('as')
                var, point = limit_info.split('->')
                expr = sp.sympify(expr_str.strip())
                var_sym = sp.Symbol(var.strip())
                val = float(point.strip())
                return f"Limit: {sp.limit(expr, var_sym, val)}"
            return "Usage: limit sin(x)/x as x->0"
        except Exception as e:
            return f"Error: {e}"
    
    @staticmethod
    def get_help() -> str:
        return """
📈 CALCULUS:
  derivative x**2     - Derivative
  integral x**2       - Indefinite integral
  limit sin(x)/x as x->0 - Limit

"""
