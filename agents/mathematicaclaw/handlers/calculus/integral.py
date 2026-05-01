"""Step-by-step integral computation"""
import sympy as sp
import re
from sympy import symbols, integrate, sympify, pretty

x = symbols('x')

def integral(args=None):
    if not args:
        return "Usage: /integral 2*x**3 + 5*x  OR  /integral x**2 from 0 to 1"
    try:
        expr_str = args.strip()
        if ' from ' in expr_str.lower():
            parts = expr_str.lower().split(' from ')
            expr = sympify(parts[0].strip())
            bounds = re.match(r'(.+?)\s+to\s+(.+)', parts[1])
            if bounds:
                lower = sympify(bounds.group(1))
                upper = sympify(bounds.group(2))
                antideriv = integrate(expr, x)
                result = integrate(expr, (x, lower, upper))
                steps = [
                    f"Find \u222b[{lower} to {upper}] ({parts[0].strip()}) dx", "",
                    "Step 1: Find antiderivative F(x)",
                    f"  F(x) = {pretty(antideriv)}", "",
                    "Step 2: Apply Fundamental Theorem of Calculus",
                    f"  F({upper}) - F({lower}) = {pretty(result)}", "",
                    f"Result: {pretty(result)}"
                ]
                return "\n".join(steps)
        expr = sympify(expr_str)
        result = integrate(expr, x)
        steps = [f"Find \u222b({expr_str}) dx", ""]
        if expr.is_Pow:
            steps.append(f"Power Rule: \u222bx^n dx = x^(n+1)/(n+1) + C")
        elif expr.func == sp.sin:
            steps.append("Rule: \u222bsin(x) dx = -cos(x) + C")
        elif expr.func == sp.cos:
            steps.append("Rule: \u222bcos(x) dx = sin(x) + C")
        elif expr.func == sp.exp:
            steps.append("Rule: \u222be^x dx = e^x + C")
        else:
            steps.append("Applying integration rules")
        steps.append(f"  Result: {pretty(result)}")
        steps.append("")
        steps.append(f"Final: {pretty(result)} + C")
        return "\n".join(steps)
    except Exception as e:
        return f"Error: {e}"
