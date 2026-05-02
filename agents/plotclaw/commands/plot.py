"""Plot command - Mathematical function plotting with full styling"""
import os
from pathlib import Path

name = "plot"
description = "Plot mathematical functions"

def parse_flags(args):
    flags = {}
    remaining = []
    parts = args.split()
    i = 0
    while i < len(parts):
        if parts[i].startswith("--"):
            key = parts[i][2:]
            if i + 1 < len(parts) and not parts[i+1].startswith("--"):
                flags[key] = parts[i+1]
                i += 2
            else:
                flags[key] = True
                i += 1
        else:
            remaining.append(parts[i])
            i += 1
    return " ".join(remaining), flags

def run(args):
    if not args:
        return "Usage: /plot <expr> [--range min,max] [--legend] [--title Title] [--xlabel X] [--ylabel Y] [--annotate text,x,y] [--theme dark] [--format svg|pdf|png] [--save-only]
Example: /plot sin(x),cos(x) --range -pi,pi --legend --annotate peak,1.57,1"

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np

        clean_args, flags = parse_flags(args)

        # Parse: can be "sin(x),cos(x) --range -pi,pi" or "sin(x) -5,5"
        parts = clean_args.split()
        expr_part = parts[0] if parts else clean_args
        range_part = parts[1] if len(parts) > 1 else None

        # Range parsing
        x_min, x_max = -10, 10
        if range_part and not range_part.startswith("--"):
            range_clean = range_part.strip('[]()')
            if ',' in range_clean:
                try:
                    x_min, x_max = map(float, range_clean.split(','))
                except:
                    pass
        elif flags.get("range"):
            r = flags["range"].strip('[]()')
            try:
                x_min, x_max = map(float, r.split(','))
            except:
                pass

        # Theme
        if flags.get("theme") == "dark":
            plt.style.use('dark_background')
        else:
            plt.style.use('default')

        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.linspace(x_min, x_max, 1000)

        # Multi-function support: sin(x),cos(x)
        expressions = [e.strip() for e in expr_part.split(',')]
        colors = ['steelblue', 'coral', 'seagreen', 'goldenrod', 'purple', 'cyan']

        import sympy as sp
        for i, expr in enumerate(expressions):
            expr_clean = expr.replace('^', '**')
            try:
                # Try sympy parsing
                x_sym = sp.Symbol("x")
                y_sym = sp.sympify(expr_clean)
                y = sp.lambdify(x_sym, y_sym, "numpy")(x)
            except:
                # Fallback: eval with numpy namespace
                namespace = {"x": x, "np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan, "exp": np.exp, "log": np.log, "sqrt": np.sqrt, "pi": np.pi, "abs": np.abs}
                y = eval(expr_clean, {"__builtins__": {}}, namespace)

            color = colors[i % len(colors)]
            ax.plot(x, y, linewidth=2, color=color, label=expr)

        # Legend
        if flags.get("legend") or len(expressions) > 1:
            ax.legend(fontsize=10)

        # Annotations
        annotate = flags.get("annotate", "")
        if annotate:
            parts_a = annotate.split(",")
            if len(parts_a) >= 3:
                text, ax_x, ax_y = parts_a[0], float(parts_a[1]), float(parts_a[2])
                ax.annotate(text, xy=(ax_x, ax_y), xytext=(ax_x+0.5, ax_y+0.5),
                           arrowprops=dict(arrowstyle='->', color='red'), fontsize=10, color='red')

        ax.set_title(flags.get("title", f"Plot: {expr_part}"), fontsize=14, fontweight='bold')
        ax.set_xlabel(flags.get("xlabel", "x"), fontsize=11)
        ax.set_ylabel(flags.get("ylabel", "f(x)"), fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='gray', linewidth=0.5)
        ax.axvline(x=0, color='gray', linewidth=0.5)

        fmt = flags.get("format", "png").lower().strip(".")
        agent_dir = Path(__file__).parent.parent
        exports_dir = agent_dir / "exports"
        exports_dir.mkdir(exist_ok=True)
        path = exports_dir / f"plot_{hash(expr_part)%100000}.{fmt}"
        plt.savefig(str(path), dpi=150, bbox_inches='tight')
        plt.close()

        if os.path.exists(str(path)):
            if not flags.get("save-only"):
                os.startfile(str(path))
            return f"[OK] Plot saved -> {path}"
        return "[FAIL] Could not save plot"

    except ImportError:
        return "[FAIL] matplotlib/numpy/sympy not installed"
    except Exception as e:
        return f"[FAIL] {e}"