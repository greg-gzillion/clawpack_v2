"""Calculus handlers - derivative, integral, limit, proof"""
import sympy as sp
from sympy import symbols, diff, integrate, limit, sympify, pretty
x = symbols('x')

def derivative(args=None):
    if not args: return "Usage: /derivative x**4 + 3*x**2"
    try:
        expr = sympify(args)
        return f"Derivative: {pretty(diff(expr, x))}"
    except Exception as e:
        return f"Error: {e}"

def integral(args=None):
    if not args: return "Usage: /integral 2*x**3 + 5*x"
    try:
        expr = sympify(args)
        return f"Integral: {pretty(integrate(expr, x))} + C"
    except Exception as e:
        return f"Error: {e}"

def limit_func(args=None):
    if not args: return "Usage: /limit sin(x)/x, 0"
    try:
        parts = args.split(',')
        expr = sympify(parts[0].strip())
        point = sympify(parts[1].strip()) if len(parts) > 1 else 0
        result = limit(expr, x, point)
        return f"lim = {pretty(result)}"
    except Exception as e:
        return f"Error: {e}"

def proof(statement=None):
    if not statement: return "Usage: /proof sqrt(2) is irrational"
    try:
        from shared.llm import get_llm_client
        client = get_llm_client()
        prompt = f"Prove this mathematical statement rigorously: {statement}"
        response = client.call_sync(prompt=prompt, agent='mathematicaclaw', capability='math_proof')
        return "PROOF: " + statement + chr(10)*2 + response.content

{response.content}"
    except Exception as e:
        return f"Proof unavailable: {e}"

__all__ = ['derivative', 'integral', 'limit_func', 'proof']