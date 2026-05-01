from pathlib import Path
base = Path(r'C:\Users\greg\dev\clawpack_v2\agents\mathematicaclaw\handlers\calculus')

# integral.py
(base / 'integral.py').write_text('''"""Step-by-step integral computation"""
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
            bounds = re.match(r'(.+?)\\s+to\\s+(.+)', parts[1])
            if bounds:
                lower = sympify(bounds.group(1))
                upper = sympify(bounds.group(2))
                antideriv = integrate(expr, x)
                result = integrate(expr, (x, lower, upper))
                steps = [
                    f"Find \\u222b[{lower} to {upper}] ({parts[0].strip()}) dx", "",
                    "Step 1: Find antiderivative F(x)",
                    f"  F(x) = {pretty(antideriv)}", "",
                    "Step 2: Apply Fundamental Theorem of Calculus",
                    f"  F({upper}) - F({lower}) = {pretty(result)}", "",
                    f"Result: {pretty(result)}"
                ]
                return "\\n".join(steps)
        expr = sympify(expr_str)
        result = integrate(expr, x)
        steps = [f"Find \\u222b({expr_str}) dx", ""]
        if expr.is_Pow:
            steps.append(f"Power Rule: \\u222bx^n dx = x^(n+1)/(n+1) + C")
        elif expr.func == sp.sin:
            steps.append("Rule: \\u222bsin(x) dx = -cos(x) + C")
        elif expr.func == sp.cos:
            steps.append("Rule: \\u222bcos(x) dx = sin(x) + C")
        elif expr.func == sp.exp:
            steps.append("Rule: \\u222be^x dx = e^x + C")
        else:
            steps.append("Applying integration rules")
        steps.append(f"  Result: {pretty(result)}")
        steps.append("")
        steps.append(f"Final: {pretty(result)} + C")
        return "\\n".join(steps)
    except Exception as e:
        return f"Error: {e}"
''', encoding='utf-8')

# limit.py
(base / 'limit.py').write_text('''"""Limit computation"""
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
        steps = [f"Find lim(x\\u2192{point}) {pretty(expr)}", ""]
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
        return "\\n".join(steps)
    except Exception as e:
        return f"Error: {e}"
''', encoding='utf-8')

# proof.py
(base / 'proof.py').write_text('''"""Mathematical proof generation via LLM"""
def proof(statement=None):
    if not statement:
        return "Usage: /proof sqrt(2) is irrational"
    try:
        from shared.llm import get_llm_client
        client = get_llm_client()
        prompt = "Prove this mathematical statement rigorously with clear logical steps: " + statement
        response = client.call_sync(prompt=prompt, agent='mathematicaclaw', capability='math_proof')
        return "PROOF: " + statement + chr(10)*2 + response.content
    except Exception as e:
        return "Proof unavailable: " + str(e)
''', encoding='utf-8')

print('integral.py, limit.py, proof.py written')
