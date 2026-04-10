"""Add tool - self-describing arithmetic tool"""
import json

def get_schema():
    return {
        "name": "add",
        "description": "Add numbers together",
        "parameters": {
            "type": "object",
            "properties": {
                "numbers": {"type": "array", "items": {"type": "number"}}
            }
        }
    }

def is_concurrency_safe() -> bool:
    return True  # Add is pure, no side effects

def requires_permission() -> bool:
    return False  # No permission needed

async def execute(args: str) -> str:
    try:
        nums = [float(x) for x in args.split()]
        return f"Sum: {sum(nums)}"
    except:
        return "Usage: add 2 3 4"
