"""Arithmetic commands for mathematicaclaw"""

def add(args=None):
    """Add numbers: add 2 3 4"""
    if args:
        try:
            numbers = [float(x) for x in args.split()]
            result = sum(numbers)
            return f"Sum: {result}"
        except:
            return "Error: Invalid numbers"
    return "Usage: add 2 3 4"

def subtract(args=None):
    """Subtract numbers: subtract 10 3"""
    if args:
        try:
            numbers = [float(x) for x in args.split()]
            result = numbers[0] - sum(numbers[1:])
            return f"Result: {result}"
        except:
            return "Error: Invalid numbers"
    return "Usage: subtract 10 3"

def multiply(args=None):
    """Multiply numbers: multiply 2 3 4"""
    if args:
        try:
            numbers = [float(x) for x in args.split()]
            result = 1
            for n in numbers:
                result *= n
            return f"Product: {result}"
        except:
            return "Error: Invalid numbers"
    return "Usage: multiply 2 3 4"

def divide(args=None):
    """Divide numbers: divide 10 2"""
    if args:
        try:
            numbers = [float(x) for x in args.split()]
            result = numbers[0]
            for n in numbers[1:]:
                result /= n
            return f"Result: {result}"
        except:
            return "Error: Invalid numbers"
    return "Usage: divide 10 2"

def power(args=None):
    """Power: power 2 3 = 2^3"""
    if args:
        try:
            a, b = args.split()
            result = float(a) ** float(b)
            return f"{a}^{b} = {result}"
        except:
            return "Error: Invalid input"
    return "Usage: power 2 3"

def sqrt(args=None):
    """Square root: sqrt 16"""
    if args:
        try:
            import math
            result = math.sqrt(float(args))
            return f"√{args} = {result}"
        except:
            return "Error: Invalid number"
    return "Usage: sqrt 16"

def percent(args=None):
    """Percentage: percent 50 of 200"""
    if args:
        try:
            parts = args.split()
            if len(parts) == 3 and parts[1] == 'of':
                pct = float(parts[0])
                total = float(parts[2])
                result = (pct / 100) * total
                return f"{pct}% of {total} = {result}"
        except:
            return "Error: Invalid input"
    return "Usage: percent 50 of 200"
