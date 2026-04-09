"""Mathematicaclaw Agent - Main coordinator"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.engine import MathEngine
from core.session_manager import SessionManager

class MathematicaclawAgent:
    """Mathematical computation AI agent"""
    
    def __init__(self):
        self.engine = MathEngine()
        self.session = SessionManager()
    
    def solve(self, equation: str, variable: str = 'x'):
        """Solve an equation"""
        result = self.engine.solve_equation(equation, variable)
        self.session.add_query("solve", equation)
        return result
    
    def derivative(self, expression: str, variable: str = 'x', order: int = 1):
        """Calculate derivative"""
        result = self.engine.derivative(expression, variable, order)
        self.session.add_query("derivative", expression)
        return result
    
    def integral(self, expression: str, variable: str = 'x', a=None, b=None):
        """Calculate integral"""
        definite = (a, b) if a is not None and b is not None else None
        result = self.engine.integral(expression, variable, definite)
        self.session.add_query("integral", expression)
        return result
    
    def simplify(self, expression: str):
        """Simplify expression"""
        result = self.engine.simplify(expression)
        self.session.add_query("simplify", expression)
        return result
    
    def factor(self, expression: str):
        """Factor expression"""
        result = self.engine.factor(expression)
        self.session.add_query("factor", expression)
        return result
    
    def expand(self, expression: str):
        """Expand expression"""
        result = self.engine.expand(expression)
        self.session.add_query("expand", expression)
        return result
    
    def matrix(self, matrix_data: list, operation: str, **kwargs):
        """Matrix operations"""
        result = self.engine.matrix_operations(matrix_data, operation, **kwargs)
        self.session.add_query("matrix", f"{operation}")
        return result
    
    def stats(self, data: list):
        """Calculate statistics"""
        result = self.engine.statistics(data)
        self.session.add_query("stats", f"{len(data)} values")
        return result
    
    def evaluate(self, expression: str, values: dict):
        """Evaluate expression"""
        result = self.engine.evaluate(expression, values)
        self.session.add_query("evaluate", expression)
        return result
    
    def solve_system(self, equations: list, variables: list):
        """Solve system of equations"""
        result = self.engine.solve_system(equations, variables)
        self.session.add_query("system", f"{len(equations)} eqs")
        return result
    
    def limit(self, expression: str, variable: str, point: float):
        """Calculate limit"""
        result = self.engine.limit(expression, variable, point)
        self.session.add_query("limit", expression)
        return result
    
    def series(self, expression: str, variable: str, point: float = 0, order: int = 6):
        """Calculate series expansion"""
        result = self.engine.series(expression, variable, point, order)
        self.session.add_query("series", expression)
        return result
    
    def get_stats(self):
        """Get session statistics"""
        return self.session.get_stats()
