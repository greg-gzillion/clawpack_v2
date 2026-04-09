#!/usr/bin/env python3
"""SVG Drawer - Pure vector graphics generation"""

import math
from typing import Dict, List, Tuple, Optional
import base64
from io import BytesIO

class SVGDrawer:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.elements = []
    
    def draw(self, specs: Dict) -> Dict:
        """Create SVG drawing based on specifications"""
        try:
            self.width = specs.get("width", 800)
            self.height = specs.get("height", 600)
            elements = specs.get("elements", [])
            background = specs.get("background", "white")
            
            svg_content = self._build_svg(elements, background)
            
            # Convert to base64 for embedding
            svg_bytes = svg_content.encode('utf-8')
            img_base64 = base64.b64encode(svg_bytes).decode()
            
            return {
                "success": True,
                "svg": svg_content,
                "base64": img_base64,
                "type": "svg",
                "width": self.width,
                "height": self.height
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _build_svg(self, elements: List[Dict], background: str) -> str:
        """Build SVG content from elements"""
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="{self.width}" height="{self.height}">\n'
        
        if background != "none":
            svg += f'  <rect width="{self.width}" height="{self.height}" fill="{background}"/>\n'
        
        for elem in elements:
            elem_type = elem.get("type")
            
            if elem_type == "rect":
                svg += self._draw_rect(elem)
            elif elem_type == "circle":
                svg += self._draw_circle(elem)
            elif elem_type == "line":
                svg += self._draw_line(elem)
            elif elem_type == "polygon":
                svg += self._draw_polygon(elem)
            elif elem_type == "text":
                svg += self._draw_text(elem)
            elif elem_type == "path":
                svg += self._draw_path(elem)
            elif elem_type == "ellipse":
                svg += self._draw_ellipse(elem)
        
        svg += '</svg>'
        return svg
    
    def _draw_rect(self, elem: Dict) -> str:
        x = elem.get("x", 0)
        y = elem.get("y", 0)
        w = elem.get("width", 100)
        h = elem.get("height", 100)
        fill = elem.get("fill", "blue")
        stroke = elem.get("stroke", "black")
        stroke_width = elem.get("stroke_width", 1)
        rx = elem.get("rx", 0)
        
        return f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" rx="{rx}"/>\n'
    
    def _draw_circle(self, elem: Dict) -> str:
        cx = elem.get("cx", 400)
        cy = elem.get("cy", 300)
        r = elem.get("r", 50)
        fill = elem.get("fill", "red")
        stroke = elem.get("stroke", "black")
        stroke_width = elem.get("stroke_width", 1)
        
        return f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>\n'
    
    def _draw_line(self, elem: Dict) -> str:
        x1 = elem.get("x1", 0)
        y1 = elem.get("y1", 0)
        x2 = elem.get("x2", 100)
        y2 = elem.get("y2", 100)
        stroke = elem.get("stroke", "black")
        stroke_width = elem.get("stroke_width", 2)
        
        return f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{stroke_width}"/>\n'
    
    def _draw_polygon(self, elem: Dict) -> str:
        points = elem.get("points", [])
        points_str = " ".join([f"{p[0]},{p[1]}" for p in points])
        fill = elem.get("fill", "green")
        stroke = elem.get("stroke", "black")
        stroke_width = elem.get("stroke_width", 1)
        
        return f'  <polygon points="{points_str}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>\n'
    
    def _draw_text(self, elem: Dict) -> str:
        x = elem.get("x", 10)
        y = elem.get("y", 30)
        text = elem.get("text", "Text")
        font_size = elem.get("font_size", 16)
        fill = elem.get("fill", "black")
        text_anchor = elem.get("text_anchor", "start")
        
        return f'  <text x="{x}" y="{y}" font-size="{font_size}" fill="{fill}" text-anchor="{text_anchor}">{text}</text>\n'
    
    def _draw_path(self, elem: Dict) -> str:
        d = elem.get("d", "")
        fill = elem.get("fill", "none")
        stroke = elem.get("stroke", "black")
        stroke_width = elem.get("stroke_width", 2)
        
        return f'  <path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>\n'
    
    def _draw_ellipse(self, elem: Dict) -> str:
        cx = elem.get("cx", 400)
        cy = elem.get("cy", 300)
        rx = elem.get("rx", 100)
        ry = elem.get("ry", 50)
        fill = elem.get("fill", "orange")
        stroke = elem.get("stroke", "black")
        stroke_width = elem.get("stroke_width", 1)
        
        return f'  <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>\n'
    
    def create_arrow(self, x1: float, y1: float, x2: float, y2: float, 
                     color: str = "black", width: int = 2) -> Dict:
        """Create an arrow element"""
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_size = 15
        
        # Arrow head points
        x3 = x2 - arrow_size * math.cos(angle - 0.3)
        y3 = y2 - arrow_size * math.sin(angle - 0.3)
        x4 = x2 - arrow_size * math.cos(angle + 0.3)
        y4 = y2 - arrow_size * math.sin(angle + 0.3)
        
        elements = [
            {"type": "line", "x1": x1, "y1": y1, "x2": x2, "y2": y2, "stroke": color, "stroke_width": width},
            {"type": "polygon", "points": [(x2, y2), (x3, y3), (x4, y4)], "fill": color}
        ]
        
        return {"elements": elements}
