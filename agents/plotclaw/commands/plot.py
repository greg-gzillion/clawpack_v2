"""Plot command - Line charts"""

import os
from pathlib import Path

name = "plot"
description = "Create line plot"

def run(args):
    if not args:
        return "Usage: /plot <expression> [range]\nExample: /plot sin(x) -5,5"
    
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
        
        parts = args.split()
        expr = parts[0]
        
        if len(parts) > 1:
            range_part = parts[1].strip('[]()')
            if ',' in range_part:
                x_min, x_max = map(float, range_part.split(','))
            else:
                x_min, x_max = -5, 5
        else:
            x_min, x_max = -5, 5
        
        x = np.linspace(x_min, x_max, 500)
        namespace = {"x": x, "np": np, "sin": np.sin, "cos": np.cos}
        
        expr_clean = expr.replace('^', '**')
        import sympy as sp; x_sym = sp.Symbol("x"); y_sym = sp.sympify(expr_clean); y = sp.lambdify(x_sym, y_sym, "numpy")(x)
        
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, linewidth=2, color='steelblue')
        plt.title(f"Plot: {expr}")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True, alpha=0.3)
        
        # FIXED: Use absolute path
        agent_dir = Path(__file__).parent.parent
        exports_dir = agent_dir / "exports"
        exports_dir.mkdir(exist_ok=True)
        
        path = exports_dir / f"plot_{hash(args)%10000}.png"
        plt.savefig(str(path), dpi=150, bbox_inches='tight')
        plt.close()
        
        if os.path.exists(str(path)):
            os.startfile(str(path))
            return f"📈 Plot created! Opening..."
        else:
            return f"❌ Failed to save plot"
        
    except ImportError:
        return "❌ matplotlib/numpy not installed. Run: pip install matplotlib numpy"
    except Exception as e:
        return f"❌ Error: {e}"
