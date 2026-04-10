"""Plotting commands for visualization"""
from typing import Dict, Callable

class PlotCommands:
    """All plotting-related commands"""
    
    @staticmethod
    def get_commands() -> Dict[str, Callable]:
        return {
            'plot': PlotCommands._plot,
        }
    
    @staticmethod
    def _plot(args: str) -> str:
        """Basic 2D plot: plot x**2"""
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            import sympy as sp
            
            # Parse expression
            x = sp.Symbol('x')
            expr = sp.sympify(args)
            f = sp.lambdify(x, expr, modules=['numpy'])
            
            # Generate data
            x_vals = np.linspace(-10, 10, 1000)
            y_vals = f(x_vals)
            
            # Create plot
            plt.figure(figsize=(10, 6))
            plt.plot(x_vals, y_vals, 'b-', linewidth=2)
            plt.grid(True, alpha=0.3)
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.title(f'Plot of {args}')
            plt.axhline(y=0, color='k', linewidth=0.5)
            plt.axvline(x=0, color='k', linewidth=0.5)
            
            plt.show(block=True)
            plt.close()
            
            return f"✅ Plot of '{args}' displayed"
        except Exception as e:
            return f"❌ Plot error: {str(e)}\nUsage: plot x**2"
    
    @staticmethod
    def get_help() -> str:
        return """
🎨 PLOTTING:
  plot x**2               - Basic 2D plot

"""
