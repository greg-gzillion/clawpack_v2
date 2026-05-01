"""Step-by-step derivative computation"""
import sympy as sp
from sympy import symbols, diff, sympify, pretty

x = symbols('x')

def derivative(args=None):
    if not args:
        return "Usage: /derivative x**4 + 3*x**2 - 7*x + 2"
    try:
        expr_str = args.strip()
        expr = sympify(expr_str)
        syms = list(expr.free_symbols)
        var = syms[0] if syms else x
        result = diff(expr, var)

        steps = [f"Find d/d{var}[{expr_str}]", ""]
        if expr.is_Add:
            steps.append("Sum Rule: derivative of a sum is the sum of derivatives")
            for term in expr.args:
                d = diff(term, var)
                steps.append(f"  d/d{var}[{term}] = {pretty(d)}")
        elif expr.is_Mul and len(expr.args) == 2:
            f, g = expr.args
            fp, gp = diff(f, var), diff(g, var)
            steps.append(f"Product Rule: f={f}, g={g}")
            steps.append(f"  f' = {pretty(fp)}, g' = {pretty(gp)}")
            steps.append(f"  Result: f'g + fg' = {pretty(fp*g + f*gp)}")
        elif isinstance(expr, sp.Pow):
            base, exp = expr.as_base_exp()
            steps.append(f"Power Rule: d/dx[u^n] = n*u^(n-1) * du/dx")
            steps.append(f"  n={exp}, u={base}")
        elif expr.func in [sp.sin, sp.cos, sp.tan, sp.exp, sp.log]:
            rules = {sp.sin: "cos", sp.cos: "-sin", sp.tan: "sec^2", sp.exp: "e^u", sp.log: "1/u"}
            steps.append(f"Derivative of {expr.func.__name__}: {rules.get(expr.func, 'standard rule')}")

        steps.append("")
        simplified = sp.simplify(result)
        steps.append(f"Result: d/d{var}[{expr_str}] = {pretty(simplified)}")
        return "\n".join(steps)
    except Exception as e:
        return f"Error: {e}"
