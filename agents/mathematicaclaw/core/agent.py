"""Mathematicaclaw - Mathematical computation agent"""

import sys
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.agent import BaseAgent
from shared.loop import ToolSafety
from shared.memory import MemoryType


class MathematicaclawAgent(BaseAgent):
    """Mathematical computation agent with SymPy/Numpy"""
    
    def __init__(self, project_root: Optional[Path] = None):
        super().__init__("Mathematicaclaw", project_root)
    
    def _register_tools(self):
        """Register math tools"""
        self.register_tool("solve", self.solve, ToolSafety.READ_ONLY)
        self.register_tool("derivative", self.derivative, ToolSafety.READ_ONLY)
        self.register_tool("integral", self.integral, ToolSafety.READ_ONLY)
        self.register_tool("simplify", self.simplify, ToolSafety.READ_ONLY)
        self.register_tool("factor", self.factor, ToolSafety.READ_ONLY)
        self.register_tool("expand", self.expand, ToolSafety.READ_ONLY)
        self.register_tool("evaluate", self.evaluate, ToolSafety.READ_ONLY)
        self.register_tool("stats", self.statistics, ToolSafety.READ_ONLY)
    
    def solve(self, equation: str, variable: str = "x") -> Dict:
        """Solve an equation for given variable"""
        try:
            import sympy as sp
            x = sp.Symbol(variable)
            expr = sp.sympify(equation)
            solutions = sp.solve(expr, x)
            
            result = {
                "equation": equation,
                "variable": variable,
                "solutions": [str(s) for s in solutions],
                "latex": sp.latex(solutions)
            }
            
            self.remember(
                MemoryType.FEEDBACK,
                f"Solved: {equation}",
                f"Solutions: {solutions}",
                f"Equation: {equation}\nSolutions: {solutions}"
            )
            
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def derivative(self, expression: str, variable: str = "x", order: int = 1) -> Dict:
        """Calculate derivative of expression"""
        try:
            import sympy as sp
            x = sp.Symbol(variable)
            expr = sp.sympify(expression)
            result = sp.diff(expr, x, order)
            
            return {
                "expression": expression,
                "derivative": str(result),
                "order": order,
                "latex": sp.latex(result)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def integral(self, expression: str, variable: str = "x") -> Dict:
        """Calculate indefinite integral"""
        try:
            import sympy as sp
            x = sp.Symbol(variable)
            expr = sp.sympify(expression)
            result = sp.integrate(expr, x)
            
            return {
                "expression": expression,
                "integral": str(result),
                "latex": sp.latex(result)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def simplify(self, expression: str) -> Dict:
        """Simplify expression"""
        try:
            import sympy as sp
            expr = sp.sympify(expression)
            result = sp.simplify(expr)
            
            return {
                "original": expression,
                "simplified": str(result),
                "latex": sp.latex(result)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def factor(self, expression: str) -> Dict:
        """Factor expression"""
        try:
            import sympy as sp
            expr = sp.sympify(expression)
            result = sp.factor(expr)
            
            return {
                "expression": expression,
                "factored": str(result),
                "latex": sp.latex(result)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def expand(self, expression: str) -> Dict:
        """Expand expression"""
        try:
            import sympy as sp
            expr = sp.sympify(expression)
            result = sp.expand(expr)
            
            return {
                "expression": expression,
                "expanded": str(result),
                "latex": sp.latex(result)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def evaluate(self, expression: str, values: Dict[str, float]) -> Dict:
        """Evaluate expression with given values"""
        try:
            import sympy as sp
            expr = sp.sympify(expression)
            result = expr.subs(values)
            
            return {
                "expression": expression,
                "values": values,
                "result": float(result) if result.is_number else str(result),
                "latex": sp.latex(result)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def statistics(self, data: List[float]) -> Dict:
        """Calculate basic statistics"""
        try:
            import numpy as np
            arr = np.array(data)
            
            return {
                "mean": float(np.mean(arr)),
                "median": float(np.median(arr)),
                "std": float(np.std(arr)),
                "variance": float(np.var(arr)),
                "min": float(np.min(arr)),
                "max": float(np.max(arr)),
                "count": len(data)
            }
        except Exception as e:
            return {"error": str(e)}


# Register the agent
from shared.agent import ClawpackAgentRegistry
ClawpackAgentRegistry.register("mathematicaclaw", MathematicaclawAgent)
