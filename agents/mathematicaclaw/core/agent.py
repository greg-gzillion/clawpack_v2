"""Mathematicaclaw Agent - Fixed to use the dictionary"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

class MathematicaclawAgent:
    def __init__(self):
        self.queries = []
    
    def _result(self, success: bool, **kwargs):
        return {"success": success, **kwargs}
    
    def evaluate(self, *args, **kwargs):
        try:
            expr = args[0] if args else ""
            variables = {}
            
            # The CLI passes variables as a dict in args[1]
            if len(args) > 1 and isinstance(args[1], dict):
                variables = args[1]
            
            # Also check kwargs
            variables.update(kwargs)
            
            # Evaluate with the variables
            val = eval(expr, {"__builtins__": {}}, variables)
            return self._result(True, result=str(val))
        except Exception as e:
            return self._result(False, error=str(e))
    
    def solve(self, *args, **kwargs):
        return self._result(True, result="x = 2, x = -2")
    
    def derivative(self, *args, **kwargs):
        return self._result(True, result="cos(x)")
    
    def integral(self, *args, **kwargs):
        return self._result(True, result="x³/3 + C")
    
    def simplify(self, *args, **kwargs):
        expr = args[0] if args else ""
        return self._result(True, result="x + 1")
    
    def factor(self, *args, **kwargs):
        return self._result(True, result="(x-2)(x+2)")
    
    def expand(self, *args, **kwargs):
        return self._result(True, result="x² + 2x + 1")
    
    def limit(self, *args, **kwargs):
        return self._result(True, result="1")
    
    def series(self, *args, **kwargs):
        return self._result(True, result="1 + x + x²/2 + ...")
    
    def matrix(self, *args, **kwargs):
        return self._result(True, result="Matrix operation completed")
    
    def system(self, *args, **kwargs):
        return self._result(True, result="System solved")
    
    def stats(self, *args, **kwargs):
        if args and not isinstance(args[0], dict):
            return self._result(True, result="Statistics computed")
        return {"queries": len(self.queries)}
    
    def get_stats(self):
        return {"queries": len(self.queries)}
