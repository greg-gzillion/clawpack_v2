def run(args):
    """Plot a mathematical function and open in browser"""
    if not args:
        return "Usage: /plot x**2"

    try:
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend
        import matplotlib.pyplot as plt
        import numpy as np
        import sympy as sp
        import webbrowser
        from pathlib import Path

        x = sp.Symbol('x')
        expr = sp.sympify(args)
        f = sp.lambdify(x, expr, modules=['numpy'])

        x_vals = np.linspace(-10, 10, 1000)
        y_vals = f(x_vals)

        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, y_vals, 'b-', linewidth=2)
        plt.grid(True, alpha=0.3)
        plt.title(f'f(x) = {args}')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.axhline(y=0, color='k', linewidth=0.5)
        plt.axvline(x=0, color='k', linewidth=0.5)
        
        # Save to exports folder
        export_dir = Path("exports")
        export_dir.mkdir(exist_ok=True)
        filename = export_dir / f"plot_{args.replace('*','x').replace(' ','_')[:30]}.png"
        plt.savefig(str(filename), dpi=100, bbox_inches='tight')
        plt.close()
        
        # Open in browser
        webbrowser.open(str(filename.absolute()))
        
        return f"Plot saved and opened: {filename}"
    except Exception as e:
        return f"Plot error: {e}"
