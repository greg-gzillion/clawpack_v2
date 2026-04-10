"""Handles mathematical plotting with pop-up windows"""
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from typing import Tuple, Optional
import tempfile
import os

class Plotter:
    """Create and display mathematical plots in pop-up windows"""
    
    @staticmethod
    def plot_function(expression: str, x_range: Tuple[float, float] = (-10, 10), 
                      title: str = None, show_grid: bool = True) -> str:
        """Plot a mathematical function in a pop-up window"""
        try:
            # Parse expression
            x = sp.Symbol('x')
            expr = sp.sympify(expression)
            
            # Convert to lambda function
            f = sp.lambdify(x, expr, modules=['numpy'])
            
            # Generate x values
            x_vals = np.linspace(x_range[0], x_range[1], 1000)
            
            # Handle potential errors (division by zero, etc.)
            with np.errstate(divide='ignore', invalid='ignore'):
                y_vals = f(x_vals)
                # Replace inf/nan with NaN for clean plotting
                y_vals = np.where(np.isfinite(y_vals), y_vals, np.nan)
            
            # Create figure
            plt.figure(figsize=(12, 8))
            plt.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {expression}')
            
            # Add styling
            if show_grid:
                plt.grid(True, alpha=0.3)
            
            plt.xlabel('x', fontsize=12)
            plt.ylabel('f(x)', fontsize=12)
            
            if title:
                plt.title(title, fontsize=14, fontweight='bold')
            else:
                plt.title(f'Plot of {expression}', fontsize=14, fontweight='bold')
            
            plt.legend(loc='best')
            plt.axhline(y=0, color='k', linewidth=0.5)
            plt.axvline(x=0, color='k', linewidth=0.5)
            
            # Set limits
            y_vals_clean = y_vals[~np.isnan(y_vals)]
            if len(y_vals_clean) > 0:
                y_min, y_max = y_vals_clean.min(), y_vals_clean.max()
                y_padding = (y_max - y_min) * 0.1
                plt.ylim(y_min - y_padding, y_max + y_padding)
            
            plt.xlim(x_range[0], x_range[1])
            
            # Show the plot in a pop-up window
            plt.show(block=True)
            plt.close()
            
            return f"✅ Plot of '{expression}' displayed"
            
        except Exception as e:
            return f"❌ Plot error: {str(e)}"
    
    @staticmethod
    def plot_multiple(expressions: list, x_range: Tuple[float, float] = (-10, 10),
                      title: str = "Multiple Functions") -> str:
        """Plot multiple functions on same axes"""
        try:
            x = sp.Symbol('x')
            colors = ['b', 'r', 'g', 'orange', 'purple', 'brown']
            
            plt.figure(figsize=(12, 8))
            
            for i, expr_str in enumerate(expressions):
                expr = sp.sympify(expr_str)
                f = sp.lambdify(x, expr, modules=['numpy'])
                x_vals = np.linspace(x_range[0], x_range[1], 1000)
                
                with np.errstate(divide='ignore', invalid='ignore'):
                    y_vals = f(x_vals)
                    y_vals = np.where(np.isfinite(y_vals), y_vals, np.nan)
                
                color = colors[i % len(colors)]
                plt.plot(x_vals, y_vals, color=color, linewidth=2, 
                        label=f'f(x) = {expr_str}')
            
            plt.grid(True, alpha=0.3)
            plt.xlabel('x', fontsize=12)
            plt.ylabel('f(x)', fontsize=12)
            plt.title(title, fontsize=14, fontweight='bold')
            plt.legend(loc='best')
            plt.axhline(y=0, color='k', linewidth=0.5)
            plt.axvline(x=0, color='k', linewidth=0.5)
            plt.xlim(x_range[0], x_range[1])
            
            plt.show(block=True)
            plt.close()
            
            return f"✅ Displayed {len(expressions)} plots"
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @staticmethod
    def plot_with_points(expression: str, points: list, 
                         x_range: Tuple[float, float] = (-10, 10)) -> str:
        """Plot function with highlighted points"""
        try:
            x = sp.Symbol('x')
            expr = sp.sympify(expression)
            f = sp.lambdify(x, expr, modules=['numpy'])
            
            plt.figure(figsize=(12, 8))
            
            # Plot function
            x_vals = np.linspace(x_range[0], x_range[1], 1000)
            with np.errstate(divide='ignore', invalid='ignore'):
                y_vals = f(x_vals)
                y_vals = np.where(np.isfinite(y_vals), y_vals, np.nan)
            
            plt.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {expression}')
            
            # Plot points
            for point in points:
                x_p = point[0]
                y_p = point[1] if len(point) > 1 else f(x_p)
                plt.plot(x_p, y_p, 'ro', markersize=8, label=f'({x_p}, {y_p:.2f})' if isinstance(y_p, float) else f'({x_p}, {y_p})')
            
            plt.grid(True, alpha=0.3)
            plt.xlabel('x', fontsize=12)
            plt.ylabel('f(x)', fontsize=12)
            plt.title(f'{expression} with highlighted points', fontsize=14, fontweight='bold')
            plt.legend(loc='best')
            
            plt.show(block=True)
            plt.close()
            
            return f"✅ Plot with {len(points)} points displayed"
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
