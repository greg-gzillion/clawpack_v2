"""Plot tool - self-describing visualization tool"""
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

def get_schema():
    return {
        "name": "plot",
        "description": "Plot a mathematical function",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string"}
            }
        }
    }

def is_concurrency_safe() -> bool:
    return False  # Plot uses display, can't run concurrent

def requires_permission() -> bool:
    return False

async def execute(args: str) -> str:
    try:
        x = sp.Symbol('x')
        expr = sp.sympify(args)
        f = sp.lambdify(x, expr, modules=['numpy'])
        x_vals = np.linspace(-10, 10, 1000)
        y_vals = f(x_vals)
        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, y_vals, 'b-', linewidth=2)
        plt.grid(True, alpha=0.3)
        plt.title(f'f(x) = {args}')
        plt.show(block=True)
        plt.close()
        return f"Plot of '{args}' displayed"
    except Exception as e:
        return f"Plot error: {e}"
