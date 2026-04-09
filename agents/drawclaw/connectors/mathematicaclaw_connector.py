"""Connector to Mathematicaclaw agent for math computations"""

import sys
from pathlib import Path
from typing import Dict, List
import json
import subprocess

class MathematicaclawConnector:
    def __init__(self):
        self.math_path = Path(__file__).parent.parent.parent / "mathematicaclaw"
        self.available = self.math_path.exists()
    
    def evaluate_function(self, expression: str, x_range: tuple, points: int = 1000) -> Dict:
        """Evaluate a function over a range using Mathematicaclaw"""
        if not self.available:
            # Fallback to local evaluation
            return self._local_evaluate(expression, x_range, points)
        
        try:
            # Call Mathematicaclaw's evaluate command
            import numpy as np
            from sympy import sympify, Symbol, lambdify
            
            x = Symbol('x')
            expr = sympify(expression)
            f = lambdify(x, expr, 'numpy')
            
            x_vals = np.linspace(x_range[0], x_range[1], points)
            y_vals = f(x_vals)
            
            return {
                "success": True,
                "data": {
                    "x": x_vals.tolist(),
                    "y": y_vals.tolist(),
                    "expression": expression
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _local_evaluate(self, expression: str, x_range: tuple, points: int) -> Dict:
        """Local fallback evaluation"""
        try:
            import numpy as np
            
            # Simple evaluation using numpy
            x_vals = np.linspace(x_range[0], x_range[1], points)
            
            # Safe evaluation of expression
            namespace = {"x": x_vals, "np": np}
            # Replace ^ with ** for Python syntax
            safe_expr = expression.replace("^", "**")
            y_vals = eval(safe_expr, {"__builtins__": {}}, namespace)
            
            return {
                "success": True,
                "data": {
                    "x": x_vals.tolist(),
                    "y": y_vals.tolist() if hasattr(y_vals, 'tolist') else [float(y_vals)] * points,
                    "expression": expression
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def compute_geometry(self, shape: str, params: Dict) -> Dict:
        """Compute geometric properties"""
        try:
            import math
            
            if shape == "circle":
                radius = params.get("radius", 1)
                return {
                    "success": True,
                    "data": {
                        "area": math.pi * radius ** 2,
                        "circumference": 2 * math.pi * radius,
                        "radius": radius
                    }
                }
            elif shape == "rectangle":
                width = params.get("width", 1)
                height = params.get("height", 1)
                return {
                    "success": True,
                    "data": {
                        "area": width * height,
                        "perimeter": 2 * (width + height),
                        "diagonal": math.sqrt(width**2 + height**2)
                    }
                }
            elif shape == "triangle":
                a = params.get("a", 1)
                b = params.get("b", 1)
                c = params.get("c", 1)
                s = (a + b + c) / 2
                area = math.sqrt(s * (s-a) * (s-b) * (s-c))
                return {
                    "success": True,
                    "data": {
                        "area": area,
                        "perimeter": a + b + c,
                        "semiperimeter": s
                    }
                }
            else:
                return {"success": False, "error": f"Unknown shape: {shape}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def solve_equation(self, equation: str) -> Dict:
        """Solve equation using Mathematicaclaw"""
        try:
            from sympy import solve, sympify, Symbol
            
            x = Symbol('x')
            expr = sympify(equation)
            solutions = solve(expr, x)
            
            return {
                "success": True,
                "solutions": [str(s) for s in solutions]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
