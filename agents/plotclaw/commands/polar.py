"""Polar command - Polar plots"""
import os
from pathlib import Path
name = "polar"

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
        return "Usage: /polar <r(theta)> [--range min,max] [--title Title] [--theme dark] [--format svg|pdf|png] [--save-only]\nExample: /polar sin(2*theta) --range 0,6.28 --theme dark"
    try:
        import matplotlib; matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
        clean_args, flags = parse_flags(args)
        expr = clean_args.split()[0] if clean_args else "sin(2*theta)"
        rng = flags.get("range", "0,6.28")
        t_min, t_max = map(float, rng.split(","))
        plt.style.use("dark_background" if flags.get("theme")=="dark" else "default")
        theta = np.linspace(t_min, t_max, 1000)
        ns = {"theta": theta, "np": np, "sin": np.sin, "cos": np.cos, "pi": np.pi, "abs": np.abs}
        r = eval(expr.replace("^","**"), {"__builtins__": {}}, ns)
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})
        ax.plot(theta, r, linewidth=2, color="steelblue")
        ax.fill(theta, r, alpha=0.2, color="steelblue")
        ax.set_title(flags.get("title", f"Polar: r = {expr}"), fontsize=14, fontweight="bold", pad=20)
        ax.grid(True)
        fmt = flags.get("format", "png").lower().strip(".")
        ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
        path = ed / f"polar_{hash(expr)%100000}.{fmt}"
        plt.savefig(str(path), dpi=150, bbox_inches="tight")
        plt.close()
        if os.path.exists(str(path)):
            if not flags.get("save-only"): os.startfile(str(path))
            return f"[OK] Polar plot -> {path}"
        return "[FAIL] Could not save"
    except ImportError:
        return "[FAIL] matplotlib/numpy not installed"
    except Exception as e:
        return f"[FAIL] {e}"
