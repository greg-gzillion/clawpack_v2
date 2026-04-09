"""Mathematicaclaw Computation Engine"""

import math
import sympy as sp
from typing import Union, List, Dict, Optional, Tuple
import numpy as np

class MathEngine:
    """Core mathematical computation engine"""
    
    def __init__(self):
        self.symbols_cache = {}
    
    def solve_equation(self, equation: str, variable: str = 'x') -> Dict:
        """Solve algebraic equation"""
        try:
            x = sp.Symbol(variable)
            expr = sp.sympify(equation)
            solutions = sp.solve(expr, x)
            return {
                "success": True,
                "equation": equation,
                "variable": variable,
                "solutions": [str(sol) for sol in solutions],
                "method": "symbolic"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def derivative(self, expression: str, variable: str = 'x', order: int = 1) -> Dict:
        """Calculate derivative"""
        try:
            x = sp.Symbol(variable)
            expr = sp.sympify(expression)
            result = sp.diff(expr, x, order)
            return {
                "success": True,
                "expression": expression,
                "derivative": str(result),
                "order": order,
                "latex": sp.latex(result)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def integral(self, expression: str, variable: str = 'x', definite: Tuple = None) -> Dict:
        """Calculate integral"""
        try:
            x = sp.Symbol(variable)
            expr = sp.sympify(expression)
            if definite:
                a, b = definite
                result = sp.integrate(expr, (x, a, b))
                result_type = "definite"
            else:
                result = sp.integrate(expr, x)
                result_type = "indefinite"
            return {
                "success": True,
                "expression": expression,
                "integral": str(result),
                "type": result_type,
                "latex": sp.latex(result)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def simplify(self, expression: str) -> Dict:
        """Simplify expression"""
        try:
            expr = sp.sympify(expression)
            simplified = sp.simplify(expr)
            return {
                "success": True,
                "original": expression,
                "simplified": str(simplified),
                "latex": sp.latex(simplified)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def factor(self, expression: str) -> Dict:
        """Factor expression"""
        try:
            expr = sp.sympify(expression)
            factored = sp.factor(expr)
            return {
                "success": True,
                "expression": expression,
                "factored": str(factored),
                "latex": sp.latex(factored)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def expand(self, expression: str) -> Dict:
        """Expand expression"""
        try:
            expr = sp.sympify(expression)
            expanded = sp.expand(expr)
            return {
                "success": True,
                "expression": expression,
                "expanded": str(expanded),
                "latex": sp.latex(expanded)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def matrix_operations(self, matrix: List[List], operation: str, **kwargs) -> Dict:
        """Perform matrix operations"""
        try:
            M = sp.Matrix(matrix)
            if operation == "det":
                result = M.det()
            elif operation == "inv":
                result = M.inv()
            elif operation == "eigenvals":
                result = M.eigenvals()
            elif operation == "eigenvects":
                result = M.eigenvects()
            elif operation == "rref":
                result = M.rref()
            elif operation == "rank":
                result = M.rank()
            elif operation == "transpose":
                result = M.T
            else:
                return {"success": False, "error": f"Unknown operation: {operation}"}
            
            return {
                "success": True,
                "operation": operation,
                "result": str(result),
                "latex": sp.latex(result) if hasattr(result, '_latex') else str(result)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def statistics(self, data: List[float]) -> Dict:
        """Calculate basic statistics"""
        try:
            import numpy as np
            arr = np.array(data)
            return {
                "success": True,
                "mean": float(np.mean(arr)),
                "median": float(np.median(arr)),
                "std": float(np.std(arr)),
                "variance": float(np.var(arr)),
                "min": float(np.min(arr)),
                "max": float(np.max(arr)),
                "sum": float(np.sum(arr)),
                "count": len(data)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def evaluate(self, expression: str, values: Dict[str, float]) -> Dict:
        """Evaluate expression with given values"""
        try:
            expr = sp.sympify(expression)
            result = expr.subs(values)
            return {
                "success": True,
                "expression": expression,
                "values": values,
                "result": float(result) if result.is_number else str(result)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def solve_system(self, equations: List[str], variables: List[str]) -> Dict:
        """Solve system of equations"""
        try:
            syms = [sp.Symbol(v) for v in variables]
            eqs = [sp.sympify(eq) for eq in equations]
            solutions = sp.solve(eqs, syms)
            return {
                "success": True,
                "equations": equations,
                "variables": variables,
                "solutions": str(solutions)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def limit(self, expression: str, variable: str, point: float, direction: str = '+') -> Dict:
        """Calculate limit"""
        try:
            x = sp.Symbol(variable)
            expr = sp.sympify(expression)
            result = sp.limit(expr, x, point, dir=direction)
            return {
                "success": True,
                "expression": expression,
                "limit": str(result),
                "point": point,
                "latex": sp.latex(result)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def series(self, expression: str, variable: str, point: float = 0, order: int = 6) -> Dict:
        """Calculate Taylor series"""
        try:
            x = sp.Symbol(variable)
            expr = sp.sympify(expression)
            result = sp.series(expr, x, point, order)
            return {
                "success": True,
                "expression": expression,
                "series": str(result),
                "point": point,
                "order": order,
                "latex": sp.latex(result)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
