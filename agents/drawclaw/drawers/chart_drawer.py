#!/usr/bin/env python3
"""Chart Drawer - Bar, pie, line, scatter charts"""

import base64
from io import BytesIO
from typing import Dict, List

class ChartDrawer:
    def __init__(self):
        pass
    
    def draw(self, chart_type: str, data: List, labels: List = None, title: str = "Chart") -> Dict:
        """Draw various chart types"""
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            if chart_type == "bar":
                return self._draw_bar(ax, data, labels, title)
            elif chart_type == "pie":
                return self._draw_pie(ax, data, labels, title)
            elif chart_type == "line":
                return self._draw_line(ax, data, labels, title)
            elif chart_type == "scatter":
                return self._draw_scatter(ax, data, labels, title)
            elif chart_type == "area":
                return self._draw_area(ax, data, labels, title)
            elif chart_type == "radar":
                return self._draw_radar(ax, data, labels, title)
            else:
                return self._draw_bar(ax, data, labels, title)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _draw_bar(self, ax, data: List, labels: List, title: str) -> Dict:
        """Draw bar chart"""
        import matplotlib.pyplot as plt
        import numpy as np
        
        if labels is None:
            labels = [f"Item {i+1}" for i in range(len(data))]
        
        colors = plt.cm.viridis(np.linspace(0, 1, len(data)))
        ax.bar(labels, data, color=colors, edgecolor='black', linewidth=1.5)
        
        ax.set_title(title)
        ax.set_ylabel("Values")
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for i, v in enumerate(data):
            ax.text(i, v + max(data)*0.01, str(v), ha='center', fontsize=9)
        
        return self._save_plot()
    
    def _draw_pie(self, ax, data: List, labels: List, title: str) -> Dict:
        """Draw pie chart"""
        import matplotlib.pyplot as plt
        
        if labels is None:
            labels = [f"Item {i+1}" for i in range(len(data))]
        
        colors = plt.cm.Set3(range(len(data)))
        wedges, texts, autotexts = ax.pie(data, labels=labels, colors=colors, 
                                           autopct='%1.1f%%', startangle=90)
        
        ax.set_title(title)
        
        return self._save_plot()
    
    def _draw_line(self, ax, data: List, labels: List, title: str) -> Dict:
        """Draw line chart"""
        if labels is None:
            labels = list(range(len(data)))
        
        ax.plot(labels, data, 'b-', linewidth=2, marker='o', markersize=6)
        ax.fill_between(labels, data, alpha=0.3)
        
        ax.set_title(title)
        ax.set_ylabel("Values")
        ax.grid(True, alpha=0.3)
        
        return self._save_plot()
    
    def _draw_scatter(self, ax, data: List, labels: List, title: str) -> Dict:
        """Draw scatter plot"""
        import numpy as np
        
        if isinstance(data[0], (list, tuple)):
            x_data = [d[0] for d in data]
            y_data = [d[1] for d in data]
        else:
            x_data = list(range(len(data)))
            y_data = data
        
        ax.scatter(x_data, y_data, s=100, c='steelblue', alpha=0.7, edgecolors='white')
        
        ax.set_title(title)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.grid(True, alpha=0.3)
        
        return self._save_plot()
    
    def _draw_area(self, ax, data: List, labels: List, title: str) -> Dict:
        """Draw area chart"""
        if labels is None:
            labels = list(range(len(data)))
        
        ax.fill_between(labels, data, alpha=0.5, color='steelblue')
        ax.plot(labels, data, 'b-', linewidth=2)
        
        ax.set_title(title)
        ax.set_ylabel("Values")
        ax.grid(True, alpha=0.3)
        
        return self._save_plot()
    
    def _draw_radar(self, ax, data: List, labels: List, title: str) -> Dict:
        """Draw radar/spider chart"""
        import numpy as np
        import matplotlib.pyplot as plt
        
        if labels is None:
            labels = [f"Dim {i+1}" for i in range(len(data))]
        
        angles = np.linspace(0, 2*np.pi, len(data), endpoint=False).tolist()
        data = data + [data[0]]
        angles += [angles[0]]
        
        ax = plt.subplot(111, projection='polar')
        ax.plot(angles, data, 'o-', linewidth=2)
        ax.fill(angles, data, alpha=0.25)
        ax.set_thetagrids(np.degrees(angles[:-1]), labels)
        ax.set_title(title)
        ax.grid(True)
        
        return self._save_plot()
    
    def _save_plot(self) -> Dict:
        """Save plot to base64"""
        import matplotlib.pyplot as plt
        from io import BytesIO
        
        buffer = BytesIO()
        plt.tight_layout()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return {
            "success": True,
            "base64": img_base64,
            "type": "chart"
        }
