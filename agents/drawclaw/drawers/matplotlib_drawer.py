#!/usr/bin/env python3
"""Matplotlib Drawer - Scientific and mathematical plots"""

import base64
from io import BytesIO
from typing import Dict, List, Tuple, Optional
import numpy as np

class MatplotlibDrawer:
    def __init__(self):
        self.use_matplotlib = self._check_matplotlib()
    
    def _check_matplotlib(self) -> bool:
        try:
            import matplotlib
            return True
        except ImportError:
            return False
    
    def draw(self, specs: Dict) -> Dict:
        """Create matplotlib drawing"""
        if not self.use_matplotlib:
            return {"success": False, "error": "Matplotlib not installed. Run: pip install matplotlib"}
        
        plot_type = specs.get("plot_type", "line")
        
        if plot_type == "function":
            return self.plot_function(specs)
        elif plot_type == "scatter":
            return self.plot_scatter(specs)
        elif plot_type == "bar":
            return self.plot_bar(specs)
        elif plot_type == "histogram":
            return self.plot_histogram(specs)
        else:
            return self.plot_function(specs)
    
    def plot_function(self, specs: Dict) -> Dict:
        """Plot mathematical functions"""
        try:
            import matplotlib.pyplot as plt
            
            data = specs.get("data", {})
            expression = specs.get("expression", "f(x)")
            title = specs.get("title", f"Plot of {expression}")
            x_range = specs.get("x_range", (-10, 10))
            style = specs.get("style", "line")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            if "x" in data and "y" in data:
                x_vals = data["x"]
                y_vals = data["y"]
                
                if style == "line":
                    ax.plot(x_vals, y_vals, linewidth=2, label=expression)
                elif style == "scatter":
                    ax.scatter(x_vals, y_vals, s=10, alpha=0.6, label=expression)
                elif style == "both":
                    ax.plot(x_vals, y_vals, linewidth=2, alpha=0.7)
                    ax.scatter(x_vals[::50], y_vals[::50], s=20, alpha=0.8, color='red')
            
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title(title)
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0, color='k', linewidth=0.5)
            ax.axvline(x=0, color='k', linewidth=0.5)
            
            # Save to base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            img_base64 = base64.b64encode(buffer.read()).decode()
            plt.close()
            
            return {
                "success": True,
                "base64": img_base64,
                "type": "matplotlib",
                "plot_type": "function"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def plot_scatter(self, specs: Dict) -> Dict:
        """Create scatter plot"""
        try:
            import matplotlib.pyplot as plt
            
            x_data = specs.get("x_data", [])
            y_data = specs.get("y_data", [])
            title = specs.get("title", "Scatter Plot")
            x_label = specs.get("x_label", "X")
            y_label = specs.get("y_label", "Y")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(x_data, y_data, alpha=0.6, s=50, c='blue', edgecolors='white')
            
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.set_title(title)
            ax.grid(True, alpha=0.3)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            img_base64 = base64.b64encode(buffer.read()).decode()
            plt.close()
            
            return {
                "success": True,
                "base64": img_base64,
                "type": "matplotlib",
                "plot_type": "scatter"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def plot_bar(self, specs: Dict) -> Dict:
        """Create bar chart"""
        try:
            import matplotlib.pyplot as plt
            
            categories = specs.get("categories", [])
            values = specs.get("values", [])
            title = specs.get("title", "Bar Chart")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = plt.cm.viridis(np.linspace(0, 1, len(categories)))
            ax.bar(categories, values, color=colors, edgecolor='black')
            
            ax.set_title(title)
            ax.set_ylabel("Values")
            ax.grid(True, alpha=0.3, axis='y')
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            img_base64 = base64.b64encode(buffer.read()).decode()
            plt.close()
            
            return {
                "success": True,
                "base64": img_base64,
                "type": "matplotlib",
                "plot_type": "bar"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def plot_histogram(self, specs: Dict) -> Dict:
        """Create histogram"""
        try:
            import matplotlib.pyplot as plt
            
            data = specs.get("data", [])
            bins = specs.get("bins", 20)
            title = specs.get("title", "Histogram")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(data, bins=bins, color='steelblue', edgecolor='black', alpha=0.7)
            
            ax.set_xlabel("Value")
            ax.set_ylabel("Frequency")
            ax.set_title(title)
            ax.grid(True, alpha=0.3, axis='y')
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            img_base64 = base64.b64encode(buffer.read()).decode()
            plt.close()
            
            return {
                "success": True,
                "base64": img_base64,
                "type": "matplotlib",
                "plot_type": "histogram"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
