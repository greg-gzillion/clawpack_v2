"""Build and display various types of graphs"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
import numpy as np
from typing import Tuple

class GraphBuilder:
    """Create specialized graph types"""
    
    @staticmethod
    def polar_plot(expression: str, theta_range: Tuple[float, float] = (0, 2*np.pi)):
        """Create polar plot"""
        try:
            theta = np.linspace(theta_range[0], theta_range[1], 1000)
            # For polar plots, evaluate r = f(theta)
            r = eval(expression.replace('theta', 'theta_val'), 
                    {'theta_val': theta, 'np': np, 'sin': np.sin, 'cos': np.cos, 'pi': np.pi})
            
            plt.figure(figsize=(10, 10))
            ax = plt.subplot(111, projection='polar')
            ax.plot(theta, r)
            ax.set_title(f'Polar Plot: r = {expression}')
            ax.grid(True)
            
            path = "exports/temp_plot.png"
            plt.savefig(path, dpi=150, bbox_inches="tight")
            plt.close()
            os.startfile(path)
            return f"✅ Polar plot displayed"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @staticmethod
    def parametric_plot(x_expr: str, y_expr: str, t_range: Tuple[float, float] = (0, 2*np.pi)):
        """Create parametric plot"""
        try:
            t = np.linspace(t_range[0], t_range[1], 1000)
            x = eval(x_expr.replace('t', 't_val'), {'t_val': t, 'np': np, 'sin': np.sin, 'cos': np.cos, 'pi': np.pi})
            y = eval(y_expr.replace('t', 't_val'), {'t_val': t, 'np': np, 'sin': np.sin, 'cos': np.cos, 'pi': np.pi})
            
            plt.figure(figsize=(12, 8))
            plt.plot(x, y, 'b-', linewidth=2)
            plt.xlabel('x(t)')
            plt.ylabel('y(t)')
            plt.title(f'Parametric Plot: x={x_expr}, y={y_expr}')
            plt.grid(True, alpha=0.3)
            plt.axis('equal')
            
            path = "exports/temp_plot.png"
            plt.savefig(path, dpi=150, bbox_inches="tight")
            plt.close()
            os.startfile(path)
            return f"✅ Parametric plot displayed"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @staticmethod
    def contour_plot(expression: str, x_range: Tuple[float, float] = (-5, 5),
                     y_range: Tuple[float, float] = (-5, 5)):
        """Create contour plot for 2-variable functions"""
        try:
            x = np.linspace(x_range[0], x_range[1], 100)
            y = np.linspace(y_range[0], y_range[1], 100)
            X, Y = np.meshgrid(x, y)
            
            # Create a safe evaluation environment
            Z = eval(expression, {'x': X, 'y': Y, 'np': np, 'sin': np.sin, 'cos': np.cos, 'exp': np.exp})
            
            plt.figure(figsize=(10, 8))
            contour = plt.contourf(X, Y, Z, levels=20, cmap='viridis')
            plt.colorbar(contour, label='f(x,y)')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title(f'Contour Plot: {expression}')
            plt.grid(True, alpha=0.3)
            
            path = "exports/temp_plot.png"
            plt.savefig(path, dpi=150, bbox_inches="tight")
            plt.close()
            os.startfile(path)
            return f"✅ Contour plot displayed"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @staticmethod
    def histogram(data: list, bins: int = 30, title: str = "Histogram"):
        """Create histogram from data"""
        try:
            plt.figure(figsize=(10, 6))
            plt.hist(data, bins=bins, edgecolor='black', alpha=0.7)
            plt.xlabel('Value')
            plt.ylabel('Frequency')
            plt.title(title)
            plt.grid(True, alpha=0.3)
            
            path = "exports/temp_plot.png"
            plt.savefig(path, dpi=150, bbox_inches="tight")
            plt.close()
            os.startfile(path)
            return f"✅ Histogram displayed"
        except Exception as e:
            return f"❌ Error: {str(e)}"
