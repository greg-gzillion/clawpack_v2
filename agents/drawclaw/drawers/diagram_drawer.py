#!/usr/bin/env python3
"""Diagram Drawer - Flowcharts, UML, Network diagrams"""

from typing import Dict, List, Tuple
import base64
from io import BytesIO

class DiagramDrawer:
    def __init__(self):
        self.use_graphviz = self._check_graphviz()
        self.use_matplotlib = self._check_matplotlib()
    
    def _check_graphviz(self) -> bool:
        try:
            import graphviz
            return True
        except ImportError:
            return False
    
    def _check_matplotlib(self) -> bool:
        try:
            import matplotlib
            return True
        except ImportError:
            return False
    
    def draw(self, diagram_type: str, elements: List[Dict], layout: str = "horizontal") -> Dict:
        """Draw various diagram types"""
        if diagram_type == "flowchart":
            return self.draw_flowchart(elements, layout)
        elif diagram_type == "network":
            return self.draw_network(elements)
        elif diagram_type == "tree":
            return self.draw_tree(elements)
        elif diagram_type == "mindmap":
            return self.draw_mindmap(elements)
        elif diagram_type == "timeline":
            return self.draw_timeline(elements)
        else:
            return self.draw_flowchart(elements, layout)
    
    def draw_flowchart(self, nodes: List[Dict], layout: str = "horizontal") -> Dict:
        """Draw flowchart using graphviz or fallback"""
        if self.use_graphviz:
            return self._draw_flowchart_graphviz(nodes, layout)
        else:
            return self._draw_flowchart_matplotlib(nodes, layout)
    
    def _draw_flowchart_graphviz(self, nodes: List[Dict], layout: str) -> Dict:
        """Draw flowchart using graphviz"""
        try:
            from graphviz import Digraph
            
            dot = Digraph(comment='Flowchart')
            dot.attr(rankdir='LR' if layout == 'horizontal' else 'TB')
            
            # Add nodes
            for node in nodes:
                node_id = node.get("id", str(hash(str(node))))
                label = node.get("label", "Node")
                shape = node.get("shape", "box")
                color = node.get("color", "lightblue")
                
                dot.node(node_id, label, shape=shape, style='filled', fillcolor=color)
            
            # Add edges
            for node in nodes:
                for target in node.get("targets", []):
                    dot.edge(node.get("id"), target)
            
            # Render to PNG
            png_data = dot.pipe(format='png')
            img_base64 = base64.b64encode(png_data).decode()
            
            return {
                "success": True,
                "base64": img_base64,
                "type": "flowchart",
                "engine": "graphviz",
                "dot_source": dot.source
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _draw_flowchart_matplotlib(self, nodes: List[Dict], layout: str) -> Dict:
        """Fallback flowchart using matplotlib"""
        try:
            import matplotlib.pyplot as plt
            import matplotlib.patches as patches
            import numpy as np
            
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Simple layout: place nodes in a grid
            n = len(nodes)
            cols = min(4, n)
            rows = (n + cols - 1) // cols
            
            positions = {}
            for i, node in enumerate(nodes):
                row = i // cols
                col = i % cols
                x = col * 3
                y = rows - row - 1
                positions[node.get("id", str(i))] = (x, y)
                
                # Draw node
                rect = patches.Rectangle((x*100 + 50, y*100 + 50), 80, 40, 
                                         linewidth=2, edgecolor='black', 
                                         facecolor=node.get("color", "lightblue"))
                ax.add_patch(rect)
                ax.text(x*100 + 90, y*100 + 70, node.get("label", f"Node {i+1}"),
                       ha='center', va='center', fontsize=10)
            
            # Draw edges
            for node in nodes:
                node_id = node.get("id", "")
                if node_id in positions:
                    x1, y1 = positions[node_id]
                    for target in node.get("targets", []):
                        if target in positions:
                            x2, y2 = positions[target]
                            ax.annotate("", xy=(x2*100+90, y2*100+50), 
                                       xytext=(x1*100+90, y1*100+90),
                                       arrowprops=dict(arrowstyle="->", lw=1.5))
            
            ax.set_xlim(0, cols * 300)
            ax.set_ylim(0, rows * 150)
            ax.set_aspect('equal')
            ax.axis('off')
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            img_base64 = base64.b64encode(buffer.read()).decode()
            plt.close()
            
            return {
                "success": True,
                "base64": img_base64,
                "type": "flowchart",
                "engine": "matplotlib"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def draw_network(self, nodes: List[Dict]) -> Dict:
        """Draw network/graph diagram"""
        try:
            import matplotlib.pyplot as plt
            import networkx as nx
            
            G = nx.Graph()
            
            # Add nodes
            for node in nodes:
                G.add_node(node.get("id"), label=node.get("label", ""))
            
            # Add edges
            for node in nodes:
                for target in node.get("targets", []):
                    G.add_edge(node.get("id"), target)
            
            fig, ax = plt.subplots(figsize=(12, 8))
            pos = nx.spring_layout(G)
            
            nx.draw(G, pos, ax=ax, with_labels=True, node_color='lightblue',
                   node_size=2000, font_size=10, font_weight='bold',
                   edge_color='gray', width=2, alpha=0.8)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            img_base64 = base64.b64encode(buffer.read()).decode()
            plt.close()
            
            return {
                "success": True,
                "base64": img_base64,
                "type": "network"
            }
        except ImportError:
            return {"success": False, "error": "NetworkX not installed. Run: pip install networkx"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def draw_tree(self, tree_data: Dict) -> Dict:
        """Draw tree diagram"""
        # Placeholder for tree drawing
        return self.draw_flowchart([tree_data], "vertical")
    
    def draw_mindmap(self, root: Dict) -> Dict:
        """Draw mind map"""
        # Convert mindmap to flowchart structure
        nodes = [root]
        return self.draw_flowchart(nodes, "radial")
    
    def draw_timeline(self, events: List[Dict]) -> Dict:
        """Draw timeline"""
        try:
            import matplotlib.pyplot as plt
            import matplotlib.dates as mdates
            from datetime import datetime
            
            fig, ax = plt.subplots(figsize=(14, 4))
            
            y_pos = 0
            for i, event in enumerate(events):
                date = event.get("date", datetime.now())
                label = event.get("label", f"Event {i+1}")
                
                ax.plot(date, y_pos, 'o', markersize=12, color='steelblue')
                ax.text(date, y_pos + 0.02, label, rotation=45, ha='right', fontsize=9)
            
            ax.set_ylim(-0.1, 0.3)
            ax.yaxis.set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            img_base64 = base64.b64encode(buffer.read()).decode()
            plt.close()
            
            return {
                "success": True,
                "base64": img_base64,
                "type": "timeline"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
