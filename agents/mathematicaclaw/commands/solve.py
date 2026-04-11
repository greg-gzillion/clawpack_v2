def run(args):
    """Solve equation"""
    try:
        import sympy as sp
        if '=' in args:
            left, right = args.split('=')
            eq = sp.Eq(sp.sympify(left.strip()), sp.sympify(right.strip()))
        else:
            eq = sp.sympify(args)
        solutions = sp.solve(eq)
        return f"Solutions: {', '.join(str(s) for s in solutions)}"
    except Exception as e:
        return f"Error: {e}"
