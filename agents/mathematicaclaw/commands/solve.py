import re

def _preprocess(expr):
    """Convert implicit multiplication to explicit for sympy (2x -> 2*x)."""
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
    expr = re.sub(r'(\d)\(', r'\1*(', expr)
    return expr

def run(args):
    """Solve equation"""
    try:
        import sympy as sp
        args = _preprocess(args)
        if '=' in args:
            left, right = args.split('=')
            eq = sp.Eq(sp.sympify(left.strip()), sp.sympify(right.strip()))
        else:
            eq = sp.sympify(args)
        solutions = sp.solve(eq)
        return f"Solutions: {', '.join(str(s) for s in solutions)}"
    except Exception as e:
        return f"Error: {e}"