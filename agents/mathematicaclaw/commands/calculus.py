"""Calculus commands for mathematicaclaw"""
import sympy as sp

def derivative(args=None):
    """Derivative: derivative x**2"""
    if args:
        try:
            parts = args.split()
            expr_str = parts[0]
            var = parts[1] if len(parts) > 1 else 'x'
            expr = sp.sympify(expr_str)
            var_sym = sp.Symbol(var)
            result = sp.diff(expr, var_sym)
            return f"Derivative: {result}"
        except Exception as e:
            return f"Error: {str(e)}"
    return "Usage: derivative x**2"

def integral(args=None):
    """Integral: integral x**2"""
    if args:
        try:
            expr = sp.sympify(args)
            result = sp.integrate(expr)
            return f"Integral: {result} + C"
        except Exception as e:
            return f"Error: {str(e)}"
    return "Usage: integral x**2"

def limit(args=None):
    """Limit: limit sin(x)/x as x->0"""
    if args and 'as' in args:
        try:
            expr_str, limit_info = args.split('as')
            var, point = limit_info.split('->')
            expr = sp.sympify(expr_str.strip())
            var_sym = sp.Symbol(var.strip())
            val = float(point.strip())
            result = sp.limit(expr, var_sym, val)
            return f"Limit: {result}"
        except Exception as e:
            return f"Error: {str(e)}"
    return "Usage: limit sin(x)/x as x->0"
