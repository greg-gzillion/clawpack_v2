"""Limit computation"""
import sympy as sp
from sympy import symbols, limit, sympify, pretty

x = symbols('x')

def limit_func(args=None):
    if not args:
        return "Usage: /limit sin(x)/x, 0"
    try:
        parts = args.split(',')
        expr = sympify(parts[0].strip())
        point = sympify(parts[1].strip()) if len(parts) > 1 else 0
        result = limit(expr, x, point)
        steps = [f"Find lim(x\u2192{point}) {pretty(expr)}", ""]
        try:
            subbed = expr.subs(x, point)
            if subbed == sp.nan or subbed == sp.zoo:
                steps.append("Direct substitution gives indeterminate form")
                simplified = sp.simplify(expr)
                if simplified != expr:
                    steps.append(f"Simplify: {pretty(simplified)}")
        except:
            pass
        steps.append(f"Result: {pretty(result)}")
        return "\n".join(steps)
    except Exception as e:
        return f"Error: {e}"
