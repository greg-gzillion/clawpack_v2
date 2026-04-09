#!/usr/bin/env python3
"""Geometry Drawer - Geometric shapes with computed properties"""

import math
from typing import Dict, List, Tuple
import base64
from io import BytesIO

class GeometryDrawer:
    def __init__(self):
        pass
    
    def draw(self, shape: str, params: Dict) -> Dict:
        """Draw geometric shapes"""
        try:
            import matplotlib.pyplot as plt
            import matplotlib.patches as patches
            from matplotlib.patches import Circle, Rectangle, Polygon, Arc
            
            fig, ax = plt.subplots(figsize=(8, 8))
            
            if shape == "circle":
                return self._draw_circle(ax, params)
            elif shape == "rectangle":
                return self._draw_rectangle(ax, params)
            elif shape == "triangle":
                return self._draw_triangle(ax, params)
            elif shape == "polygon":
                return self._draw_polygon(ax, params)
            elif shape == "arc":
                return self._draw_arc(ax, params)
            elif shape == "coordinate":
                return self._draw_coordinate(ax, params)
            else:
                return {"success": False, "error": f"Unknown shape: {shape}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _draw_circle(self, ax, params: Dict) -> Dict:
        """Draw circle"""
        import matplotlib.pyplot as plt
        
        cx = params.get("cx", 0)
        cy = params.get("cy", 0)
        radius = params.get("radius", 1)
        color = params.get("color", "blue")
        alpha = params.get("alpha", 0.5)
        
        circle = plt.Circle((cx, cy), radius, color=color, alpha=alpha, ec='black', lw=2)
        ax.add_patch(circle)
        
        # Mark center
        ax.plot(cx, cy, 'ko', markersize=5)
        ax.text(cx, cy, f'  ({cx}, {cy})', fontsize=10)
        
        # Add radius line
        ax.plot([cx, cx + radius], [cy, cy], 'r--', lw=1, label=f'r = {radius}')
        
        return self._finalize_plot(ax, f"Circle (r={radius})", (-radius-1, radius+1), (-radius-1, radius+1))
    
    def _draw_rectangle(self, ax, params: Dict) -> Dict:
        """Draw rectangle"""
        import matplotlib.patches as patches
        
        x = params.get("x", 0)
        y = params.get("y", 0)
        width = params.get("width", 2)
        height = params.get("height", 1)
        color = params.get("color", "green")
        alpha = params.get("alpha", 0.5)
        
        rect = patches.Rectangle((x, y), width, height, color=color, alpha=alpha, ec='black', lw=2)
        ax.add_patch(rect)
        
        # Label dimensions
        ax.text(x + width/2, y - 0.1, f'{width}', ha='center', fontsize=10)
        ax.text(x - 0.1, y + height/2, f'{height}', va='center', rotation=90, fontsize=10)
        
        return self._finalize_plot(ax, f"Rectangle ({width}×{height})", (-1, width+1), (-1, height+1))
    
    def _draw_triangle(self, ax, params: Dict) -> Dict:
        """Draw triangle"""
        import numpy as np
        
        points = params.get("points", [(0, 0), (2, 0), (1, 1.732)])
        color = params.get("color", "orange")
        alpha = params.get("alpha", 0.5)
        
        triangle = plt.Polygon(points, color=color, alpha=alpha, ec='black', lw=2)
        ax.add_patch(triangle)
        
        # Label vertices
        for i, (x, y) in enumerate(points):
            ax.plot(x, y, 'ko', markersize=5)
            ax.text(x, y, f'  {chr(65+i)}', fontsize=10)
        
        return self._finalize_plot(ax, "Triangle", (-1, 3), (-1, 3))
    
    def _draw_polygon(self, ax, params: Dict) -> Dict:
        """Draw regular polygon"""
        import numpy as np
        
        sides = params.get("sides", 6)
        radius = params.get("radius", 2)
        color = params.get("color", "purple")
        alpha = params.get("alpha", 0.5)
        
        angles = np.linspace(0, 2*np.pi, sides+1)[:-1]
        points = [(radius * np.cos(a), radius * np.sin(a)) for a in angles]
        
        polygon = plt.Polygon(points, color=color, alpha=alpha, ec='black', lw=2)
        ax.add_patch(polygon)
        
        return self._finalize_plot(ax, f"Regular Polygon ({sides} sides)", (-radius-1, radius+1), (-radius-1, radius+1))
    
    def _draw_arc(self, ax, params: Dict) -> Dict:
        """Draw arc"""
        import matplotlib.patches as patches
        
        cx = params.get("cx", 0)
        cy = params.get("cy", 0)
        width = params.get("width", 2)
        height = params.get("height", 2)
        angle = params.get("angle", 0)
        theta1 = params.get("theta1", 0)
        theta2 = params.get("theta2", 180)
        color = params.get("color", "red")
        
        arc = patches.Arc((cx, cy), width, height, angle=angle, theta1=theta1, theta2=theta2, 
                          color=color, lw=3)
        ax.add_patch(arc)
        
        return self._finalize_plot(ax, f"Arc", (-2, 2), (-2, 2))
    
    def _draw_coordinate(self, ax, params: Dict) -> Dict:
        """Draw coordinate system with points"""
        points = params.get("points", [])
        labels = params.get("labels", [])
        
        for i, (x, y) in enumerate(points):
            ax.plot(x, y, 'ro', markersize=8)
            label = labels[i] if i < len(labels) else f'({x}, {y})'
            ax.text(x+0.1, y+0.1, label, fontsize=10)
        
        return self._finalize_plot(ax, "Coordinate System", (-5, 5), (-5, 5))
    
    def _finalize_plot(self, ax, title: str, xlim: Tuple, ylim: Tuple) -> Dict:
        """Finalize and save the plot"""
        import matplotlib.pyplot as plt
        from io import BytesIO
        import base64
        
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', lw=0.5)
        ax.axvline(x=0, color='k', lw=0.5)
        ax.set_title(title)
        
        if ax.get_legend_handles_labels()[0]:
            ax.legend()
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return {
            "success": True,
            "base64": img_base64,
            "type": "geometry"
        }
