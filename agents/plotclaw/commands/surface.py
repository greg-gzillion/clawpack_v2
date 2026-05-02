"""Surface command - 3D surface plots"""
import os
from pathlib import Path
name = "surface"

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
        return "Usage: /surface <z=f(x,y)> [--range min,max] [--title Title] [--cmap viridis] [--format svg|pdf|png] [--save-only]\nExample: /surface sin(sqrt(x**2+y**2)) --range -5,5 --cmap magma"
    try:
        import matplotlib; matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
        clean_args, flags = parse_flags(args)
        expr = clean_args.split()[0] if clean_args else "sin(sqrt(x**2+y**2))"
        rng = flags.get("range", "-5,5")
        r_min, r_max = map(float, rng.split(","))
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection="3d")
        x = np.linspace(r_min, r_max, 100)
        y = np.linspace(r_min, r_max, 100)
        X, Y = np.meshgrid(x, y)
        ns = {"x": X, "y": Y, "np": np, "sin": np.sin, "cos": np.cos, "sqrt": np.sqrt, "exp": np.exp, "pi": np.pi, "abs": np.abs}
        Z = eval(expr.replace("^","**"), {"__builtins__": {}}, ns)
        cmap_name = flags.get("cmap", "viridis")
        surf = ax.plot_surface(X, Y, Z, cmap=cmap_name, edgecolor="none", alpha=0.9)
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=8, label="z")
        ax.set_title(flags.get("title", f"Surface: z = {expr}"), fontsize=14, fontweight="bold")
        ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
        fmt = flags.get("format", "png").lower().strip(".")
        ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
        path = ed / f"surface_{hash(expr)%100000}.{fmt}"
        plt.savefig(str(path), dpi=150, bbox_inches="tight")
        plt.close()
        if os.path.exists(str(path)):
            if not flags.get("save-only"): os.startfile(str(path))
            return f"[OK] 3D Surface -> {path}"
        return "[FAIL] Could not save"
    except ImportError:
        return "[FAIL] matplotlib/numpy not installed"
    except Exception as e:
        return f"[FAIL] {e}"
