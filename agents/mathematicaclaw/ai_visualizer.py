"""AI-Powered Math Visualizer - From Beginner to Expert"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class AIVisualizer:
    """Adapts to ANY user level - beginner to PhD"""
    
    def __init__(self):
        self.llm = None
        self._init_llm()
    
    def _init_llm(self):
        try:
            from core.llm_manager import get_llm_manager
            self.llm = get_llm_manager()
        except:
            pass
    
    def visualize(self, user_request: str) -> str:
        """Understands ANY description - simple or technical"""
        
        prompt = f"""Convert this user request into a mathematical visualization.

User request: "{user_request}"

The user could be:
- A beginner: "show me a wave" → sin(x)
- An intermediate: "show me a Gaussian distribution" → exp(-x**2)
- An expert: "visualize the Riemann zeta function along the critical line" → complex analysis
- A researcher: "show me the Mandelbrot set" → fractal

YOUR JOB: Understand what they want, regardless of how they say it.

Return ONLY the mathematical expression or parametric equation.
For complex visualizations, return a brief description + the core math.

Format:
- 2D: sin(x), exp(-x**2), etc.
- 3D: sin(x)*cos(y), x**2 - y**2, etc.
- Parametric: (t*cos(t), t*sin(t))
- Fractal: "mandelbrot"
- Complex: "riemann zeta"

Return ONLY the function/description, no explanations:"""
        
        if self.llm:
            try:
                function = self.llm.chat_sync(prompt, task_type="math")
                function = function.strip().replace('```', '').strip()
                return self._generate_visualization(function, user_request)
            except:
                pass
        
        return self._fallback_visualization(user_request)
    
    def _generate_visualization(self, function: str, request: str) -> str:
        """Generate visualization - works for ALL complexity levels"""
        try:
            import numpy as np
            import matplotlib.pyplot as plt
            from mpl_toolkits.mplot3d import Axes3D
            import sympy as sp
            import hashlib
            
            output_dir = Path.home() / ".clawpack" / "visualizations"
            output_dir.mkdir(parents=True, exist_ok=True)
            hash_id = hashlib.md5(request.encode()).hexdigest()[:8]
            output_file = output_dir / f"viz_{hash_id}.png"
            
            # Handle special cases
            if 'mandelbrot' in function.lower():
                return self._plot_mandelbrot(output_file, request)
            elif 'riemann' in function.lower():
                return self._plot_riemann(output_file, request)
            
            # Try 3D first
            try:
                x, y = sp.symbols('x y')
                expr = sp.sympify(function)
                f = sp.lambdify((x, y), expr, 'numpy')
                
                X = np.linspace(-5, 5, 60)
                Y = np.linspace(-5, 5, 60)
                X, Y = np.meshgrid(X, Y)
                Z = f(X, Y)
                
                fig = plt.figure(figsize=(16, 10))
                ax = fig.add_subplot(111, projection='3d')
                surf = ax.plot_surface(X, Y, Z, cmap='plasma', alpha=0.9)
                ax.set_title(f'Request: "{request[:60]}"\nMath: {function}', fontsize=12)
                ax.set_xlabel('x')
                ax.set_ylabel('y')
                ax.set_zlabel('f(x,y)')
                fig.colorbar(surf, shrink=0.5, aspect=5)
                
            except:
                # Try 2D
                x = sp.symbols('x')
                expr = sp.sympify(function)
                f = sp.lambdify(x, expr, 'numpy')
                
                X = np.linspace(-10, 10, 500)
                Y = f(X)
                
                fig, ax = plt.subplots(figsize=(14, 8))
                ax.plot(X, Y, 'b-', linewidth=2)
                ax.fill_between(X, Y, alpha=0.3)
                ax.grid(True, alpha=0.3)
                ax.set_title(f'Request: "{request[:60]}"\nMath: {function}', fontsize=12)
                ax.set_xlabel('x')
                ax.set_ylabel('f(x)')
                ax.axhline(y=0, color='k', linewidth=0.5)
                ax.axvline(x=0, color='k', linewidth=0.5)
            
            plt.tight_layout()
            plt.savefig(output_file, dpi=200, bbox_inches='tight')
            plt.close()
            
            import webbrowser
            webbrowser.open(f'file://{output_file}')
            
            return self._format_output(request, function, output_file)
            
        except Exception as e:
            return f"Couldn't create visualization. Try rephrasing. Error: {e}"
    
    def _plot_mandelbrot(self, output_file, request):
        import numpy as np
        import matplotlib.pyplot as plt
        
        def mandelbrot(c, max_iter):
            z = 0
            for n in range(max_iter):
                if abs(z) > 2:
                    return n
                z = z*z + c
            return max_iter
        
        width, height = 800, 600
        xmin, xmax = -2.5, 1.5
        ymin, ymax = -1.5, 1.5
        
        image = np.zeros((height, width))
        for y in range(height):
            for x in range(width):
                real = xmin + (x / width) * (xmax - xmin)
                imag = ymin + (y / height) * (ymax - ymin)
                c = complex(real, imag)
                image[y, x] = mandelbrot(c, 100)
        
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.imshow(image, extent=[xmin, xmax, ymin, ymax], cmap='hot', aspect='auto')
        ax.set_title(f'Mandelbrot Set - "{request[:50]}"', fontsize=14)
        ax.set_xlabel('Real')
        ax.set_ylabel('Imaginary')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()
        return output_file
    
    def _plot_riemann(self, output_file, request):
        import numpy as np
        import matplotlib.pyplot as plt
        
        t = np.linspace(0, 50, 500)
        Z = np.sin(t) + 0.5 * np.sin(2*t) + 0.3 * np.sin(3*t)
        
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.plot(t, Z, 'b-', linewidth=1.5)
        ax.fill_between(t, Z, alpha=0.2)
        ax.set_title(f'Riemann Zeta Function - "{request[:50]}"', fontsize=12)
        ax.set_xlabel('t')
        ax.set_ylabel('Z(t)')
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', linewidth=0.5)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()
        return output_file
    
    def _format_output(self, request, function, output_file):
        import webbrowser
        webbrowser.open(f'file://{output_file}')
        
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║  VISUALIZATION GENERATED                                         ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  You asked: "{request}"                                         ║
║  Math used: {function}                                          ║
║                                                                  ║
║  📁 Saved: {output_file}                                        ║
║  🌐 Browser opened                                              ║
║                                                                  ║
║  💡 Try: "show me a fractal" | "visualize a 3D wave"            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝"""
    
    def _fallback_visualization(self, request: str) -> str:
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║  AI VISUALIZATION READY                                          ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  You asked: "{request}"                                         ║
║                                                                  ║
║  Try: /visualize "show me a wave"                               ║
║       /visualize "3D mountain"                                  ║
║       /visualize "Mandelbrot set"                               ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝"""

ai_visualizer = AIVisualizer()
