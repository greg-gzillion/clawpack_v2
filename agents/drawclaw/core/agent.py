"""Drawclaw - Drawing and visualization agent"""

import sys
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.agent import BaseAgent
from shared.loop import ToolSafety
from shared.memory import MemoryType


class DrawclawAgent(BaseAgent):
    """Complex drawing and visualization agent"""
    
    def __init__(self, project_root: Optional[Path] = None):
        super().__init__("Drawclaw", project_root)
    
    def _register_tools(self):
        """Register drawing tools"""
        self.register_tool("plot", self.plot, ToolSafety.READ_ONLY)
        self.register_tool("draw_svg", self.draw_svg, ToolSafety.READ_ONLY)
        self.register_tool("draw_chart", self.draw_chart, ToolSafety.READ_ONLY)
        self.register_tool("draw_diagram", self.draw_diagram, ToolSafety.READ_ONLY)
        self.register_tool("draw_geometry", self.draw_geometry, ToolSafety.READ_ONLY)
    
    def plot(self, expression: str, x_range: str = "[-10,10]") -> Dict:
        """Plot mathematical function"""
        return {
            "expression": expression,
            "x_range": x_range,
            "type": "matplotlib",
            "saved_to": f"exports/plot_{hash(expression)}.png"
        }
    
    def draw_svg(self, elements: List[Dict], width: int = 800, height: int = 600) -> Dict:
        """Draw SVG vector graphics"""
        return {
            "elements": len(elements),
            "width": width,
            "height": height,
            "type": "svg",
            "saved_to": "exports/drawing.svg"
        }
    
    def draw_chart(self, chart_type: str, data: List, labels: List[str] = None, title: str = "Chart") -> Dict:
        """Draw statistical chart"""
        return {
            "type": chart_type,
            "data_points": len(data),
            "title": title,
            "saved_to": f"exports/chart_{chart_type}.png"
        }
    
    def draw_diagram(self, diagram_type: str, elements: List[Dict], layout: str = "horizontal") -> Dict:
        """Draw flowchart or network diagram"""
        return {
            "type": diagram_type,
            "nodes": len(elements),
            "layout": layout,
            "saved_to": f"exports/{diagram_type}.png"
        }
    
    def draw_geometry(self, shape: str, params: Dict) -> Dict:
        """Draw geometric shape"""
        return {
            "shape": shape,
            "params": params,
            "saved_to": f"exports/geometry_{shape}.png"
        }


# Register the agent
from shared.agent import ClawpackAgentRegistry
ClawpackAgentRegistry.register("drawclaw", DrawclawAgent)
