"""Math handler - routes to specific math operations"""
from .arithmetic import ArithmeticOps
from .algebra import AlgebraOps
from .calculus import CalculusOps
from .plotting import PlotOps

class MathHandler:
    def __init__(self):
        self.ops = {
            'add': ArithmeticOps.add,
            'subtract': ArithmeticOps.subtract,
            'multiply': ArithmeticOps.multiply,
            'divide': ArithmeticOps.divide,
            'solve': AlgebraOps.solve,
            'simplify': AlgebraOps.simplify,
            'plot': PlotOps.plot,
            'derivative': CalculusOps.derivative,
            'integral': CalculusOps.integral,
        }
    
    def process(self, cmd: str) -> str:
        """Process math command"""
        parts = cmd.split(maxsplit=1)
        op = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if op in self.ops:
            return self.ops[op](args)
        return f"Unknown: {op}. Try add, solve, plot, derivative, integral"
