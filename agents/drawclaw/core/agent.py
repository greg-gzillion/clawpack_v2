"""Drawclaw Agent - Standalone"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

class DrawclawAgent:
    def __init__(self):
        self.session = {"queries": []}
    
    def plot(self, expression: str):
        return {"expression": expression, "saved": f"exports/plot.png"}
    
    def draw_svg(self, elements: list):
        return {"elements": len(elements), "saved": "exports/drawing.svg"}
    
    def get_stats(self):
        return {"queries": len(self.session["queries"])}
