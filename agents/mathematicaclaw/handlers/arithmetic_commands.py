"""Basic arithmetic operations"""
import math
from typing import Dict, Callable

class ArithmeticCommands:
    """All arithmetic-related commands"""
    
    @staticmethod
    def get_commands() -> Dict[str, Callable]:
        return {
            'add': ArithmeticCommands._add,
            'sub': ArithmeticCommands._subtract,
            'subtract': ArithmeticCommands._subtract,
            'mul': ArithmeticCommands._multiply,
            'multiply': ArithmeticCommands._multiply,
            'div': ArithmeticCommands._divide,
            'divide': ArithmeticCommands._divide,
            'power': ArithmeticCommands._power,
            'pow': ArithmeticCommands._power,
            'sqrt': ArithmeticCommands._sqrt,
            'percent': ArithmeticCommands._percent,
        }
    
    @staticmethod
    def _add(args: str) -> str:
        try:
            nums = [float(x) for x in args.split()]
            return f"Sum: {sum(nums)}"
        except:
            return "Usage: add 2 3 4"
    
    @staticmethod
    def _subtract(args: str) -> str:
        try:
            nums = [float(x) for x in args.split()]
            result = nums[0] - sum(nums[1:])
            return f"Result: {result}"
        except:
            return "Usage: subtract 10 3"
    
    @staticmethod
    def _multiply(args: str) -> str:
        try:
            nums = [float(x) for x in args.split()]
            result = 1
            for n in nums:
                result *= n
            return f"Product: {result}"
        except:
            return "Usage: multiply 2 3 4"
    
    @staticmethod
    def _divide(args: str) -> str:
        try:
            nums = [float(x) for x in args.split()]
            result = nums[0]
            for n in nums[1:]:
                result /= n
            return f"Result: {result}"
        except:
            return "Usage: divide 10 2"
    
    @staticmethod
    def _power(args: str) -> str:
        try:
            a, b = args.split()
            result = float(a) ** float(b)
            return f"{a}^{b} = {result}"
        except:
            return "Usage: power 2 3"
    
    @staticmethod
    def _sqrt(args: str) -> str:
        try:
            result = math.sqrt(float(args))
            return f"√{args} = {result}"
        except:
            return "Usage: sqrt 16"
    
    @staticmethod
    def _percent(args: str) -> str:
        try:
            parts = args.split()
            if len(parts) == 3 and parts[1] == 'of':
                pct = float(parts[0])
                total = float(parts[2])
                result = (pct / 100) * total
                return f"{pct}% of {total} = {result}"
            return "Usage: percent 50 of 200"
        except:
            return "Usage: percent 50 of 200"
    
    @staticmethod
    def get_help() -> str:
        return """
📐 ARITHMETIC:
  add 2 3 4           - Add numbers
  subtract 10 3       - Subtract
  multiply 2 3 4      - Multiply
  divide 10 2         - Divide
  power 2 3           - Exponentiation
  sqrt 16             - Square root
  percent 50 of 200   - Percentage

"""
