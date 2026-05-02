"""Plot command - Mathematical function plotting"""
import os
from pathlib import Path
name = "plot"

def parse_flags(args):
    flags, remaining = {}, []
    parts = args.split()
    i = 0
    while i < len(parts):
        if parts[i].startswith("--"):
            key = parts[i][2:]
            if i+1 < len(parts) and not parts[i+1].startswith("--"):
                flags[key] = parts[i+1]; i += 2
            else:
                flags[key] = True; i += 1
        else:
            remaining.append(parts[i]); i += 1
    return " ".join(remaining), flags

def run(args):
    if not args:
        return "Usage: /plot <expr> [--range min,max] [--legend] [--title Title] [--xlabel X] [--ylabel Y] [--annotate text,x,y] [--theme dark] [--format svg|pdf|png] [--save-only]\nExample: /plot sin(x),cos(x) --range -6.28,6.28 --legend --annotate intersection,0.78,0.7"
    try:
        import matplotlib; matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
        clean_args, flags = parse_flags(args)
        parts = clean_args.split()
        expr_part = parts[0] if parts else clean_args
        range_part = parts[1] if len(parts) > 1 and not parts[1].startswith("--") else None
        x_min, x_max = -10, 10
        if range_part:
            rc = range_part.strip("[]()")
            try:
                if "," in rc: x_min, x_max = map(float, rc.split(","))
            except: pass
        if flags.get("range"):
            r = flags["range"].strip("[]()")
            try: x_min, x_max = map(float, r.split(","))
            except: pass
        plt.style.use("dark_background" if flags.get("theme")=="dark" else "default")
        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.linspace(x_min, x_max, 1000)
        expressions = [e.strip() for e in expr_part.split(",")]
        colors = ["steelblue", "coral", "seagreen", "goldenrod", "purple", "cyan"]
        import sympy as sp
        for i, expr in enumerate(expressions):
            expr_clean = expr.replace("^", "**")
            try:
                x_sym = sp.Symbol("x")
                y_sym = sp.sympify(expr_clean)
                y = sp.lambdify(x_sym, y_sym, "numpy")(x)
            except:
                ns = {"x": x, "np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan, "exp": np.exp, "log": np.log, "sqrt": np.sqrt, "pi": np.pi, "abs": np.abs}
                y = eval(expr_clean, {"__builtins__": {}}, ns)
            ax.plot(x, y, linewidth=2, color=colors[i%len(colors)], label=expr)
        if flags.get("legend") or len(expressions) > 1:
            ax.legend(fontsize=10)
        annotate = flags.get("annotate", "")
        if annotate:
            pa = annotate.split(",")
            if len(pa) >= 3:
                ax.annotate(pa[0], xy=(float(pa[1]), float(pa[2])), xytext=(float(pa[1])+0.5, float(pa[2])+0.5), arrowprops=dict(arrowstyle="->", color="red"), fontsize=10, color="red")
        ax.set_title(flags.get("title", f"Plot: {expr_part}"), fontsize=14, fontweight="bold")
        ax.set_xlabel(flags.get("xlabel", "x"), fontsize=11)
        ax.set_ylabel(flags.get("ylabel", "f(x)"), fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color="gray", linewidth=0.5)
        ax.axvline(x=0, color="gray", linewidth=0.5)
        fmt = flags.get("format", "png").lower().strip(".")
        ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
        path = ed / f"plot_{hash(expr_part)%100000}.{fmt}"
        plt.savefig(str(path), dpi=150, bbox_inches="tight")
        plt.close()
        if os.path.exists(str(path)):
            if not flags.get("save-only"): os.startfile(str(path))
            return f"[OK] Plot -> {path}"
        return "[FAIL] Could not save"
    except ImportError:
        return "[FAIL] matplotlib/numpy/sympy not installed"
    except Exception as e:
        return f"[FAIL] {e}"
