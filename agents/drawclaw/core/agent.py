"""Drawclaw Agent - Coordinates drawing engines and external agents"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import json

# Fix imports - use relative paths
from connectors.mathematicaclaw_connector import MathematicaclawConnector
from connectors.docuclaw_connector import DocuclawConnector
from core.session_manager import SessionManager

class DrawclawAgent:
    """Main Drawclaw agent that coordinates all drawing operations"""
    
    def __init__(self):
        self.session = SessionManager()
        self.math_connector = MathematicaclawConnector()
        self.doc_connector = DocuclawConnector()
        
        # Initialize drawing engines
        from drawers.svg_drawer import SVGDrawer
        from drawers.matplotlib_drawer import MatplotlibDrawer
        from drawers.diagram_drawer import DiagramDrawer
        from drawers.geometry_drawer import GeometryDrawer
        from drawers.chart_drawer import ChartDrawer
        
        self.svg = SVGDrawer()
        self.mpl = MatplotlibDrawer()
        self.diagram = DiagramDrawer()
        self.geometry = GeometryDrawer()
        self.chart = ChartDrawer()
        
        # Store last drawing for save/export
        self.last_drawing = None
    
    def create_drawing(self, drawing_type: str, specs: Dict) -> Dict:
        """Create a drawing based on specifications"""
        self.session.add_query("create", drawing_type)
        
        drawers = {
            "svg": self.svg,
            "matplotlib": self.mpl,
            "diagram": self.diagram,
            "geometry": self.geometry,
            "chart": self.chart
        }
        
        if drawing_type in drawers:
            result = drawers[drawing_type].draw(specs)
            if result.get("success"):
                self.last_drawing = result
            return result
        
        return {"success": False, "error": f"Unknown drawing type: {drawing_type}"}
    
    def plot_function(self, expression: str, x_range: tuple = (-10, 10)) -> Dict:
        """Plot a mathematical function"""
        self.session.add_query("plot", expression)
        
        # Get computed values from math connector
        points = self.math_connector.evaluate_function(expression, x_range)
        
        if points.get("success"):
            # Pass data to matplotlib drawer
            specs = {
                "plot_type": "function",
                "data": points["data"],
                "expression": expression,
                "x_range": x_range,
                "style": "line"
            }
            result = self.mpl.draw(specs)
            if result.get("success"):
                self.last_drawing = result
            return result
        
        return points
    
    def draw_diagram(self, diagram_type: str, elements: List[Dict], 
                     layout: str = "horizontal") -> Dict:
        """Draw diagrams (flowcharts, UML, network, etc.)"""
        self.session.add_query("diagram", diagram_type)
        result = self.diagram.draw(diagram_type, elements, layout)
        if result.get("success"):
            self.last_drawing = result
        return result
    
    def draw_geometry(self, shape: str, params: Dict) -> Dict:
        """Draw geometric shapes"""
        self.session.add_query("geometry", shape)
        
        if "compute" in params:
            computation = self.math_connector.compute_geometry(shape, params["compute"])
            if computation.get("success"):
                params.update(computation["data"])
        
        result = self.geometry.draw(shape, params)
        if result.get("success"):
            self.last_drawing = result
        return result
    
    def draw_chart(self, chart_type: str, data: List, labels: List = None,
                   title: str = "Chart") -> Dict:
        """Draw statistical charts"""
        self.session.add_query("chart", chart_type)
        result = self.chart.draw(chart_type, data, labels, title)
        if result.get("success"):
            self.last_drawing = result
        return result
    
    def export_to_docuclaw(self, drawing_id: str, format: str = "png", 
                           template: str = None) -> Dict:
        """Export drawing to Docuclaw for document integration"""
        return self.doc_connector.export_drawing(drawing_id, format, template)
    
    def save_drawing(self, filename: str, format: str = "png") -> Dict:
        """Save current drawing to file"""
        if not self.last_drawing:
            return {"success": False, "error": "No drawing to save"}
        
        export_dir = Path("exports")
        export_dir.mkdir(exist_ok=True)
        
        filepath = export_dir / f"{filename}.{format}"
        
        try:
            if "base64" in self.last_drawing:
                import base64
                img_data = base64.b64decode(self.last_drawing["base64"])
                filepath.write_bytes(img_data)
            elif "svg" in self.last_drawing:
                filepath.write_text(self.last_drawing["svg"], encoding='utf-8')
            else:
                return {"success": False, "error": "No image data to save"}
            
            self.session.add_drawing(filename, str(filepath))
            return {"success": True, "filepath": str(filepath)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_drawings(self) -> Dict:
        """List all created drawings in this session"""
        return {"success": True, "drawings": self.session.get_drawings()}
    
    def get_stats(self) -> Dict:
        """Get session statistics"""
        return self.session.get_stats()
