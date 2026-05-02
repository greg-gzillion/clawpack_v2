"""Hist command - Histogram charts"""
import os
from pathlib import Path
name = "hist"

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
        return "Usage: /hist <values> [--bins N] [--title Title] [--xlabel X] [--ylabel Y] [--theme dark] [--format svg|pdf|png] [--save-only]\nExample: /hist 1,2,2,3,3,3,4,4,4,4,5,5,5,5,5 --bins 5"
    try:
        import matplotlib; matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        clean_args, flags = parse_flags(args)
        values = [float(v.strip()) for v in clean_args.split(",")]
        bins = int(flags.get("bins", 10))
        plt.style.use("dark_background" if flags.get("theme")=="dark" else "default")
        fig, ax = plt.subplots(figsize=(9, 6))
        edge = "white" if flags.get("theme")=="dark" else "black"
        ax.hist(values, bins=bins, color="steelblue", edgecolor=edge, alpha=0.8)
        ax.set_title(flags.get("title", "Histogram"), fontsize=14, fontweight="bold")
        ax.set_xlabel(flags.get("xlabel", "Value"), fontsize=11)
        ax.set_ylabel(flags.get("ylabel", "Frequency"), fontsize=11)
        ax.grid(axis="y", alpha=0.3)
        fmt = flags.get("format", "png").lower().strip(".")
        ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
        path = ed / f"hist_{hash(str(values))%100000}.{fmt}"
        plt.savefig(str(path), dpi=150, bbox_inches="tight")
        plt.close()
        if os.path.exists(str(path)):
            if not flags.get("save-only"): os.startfile(str(path))
            return f"[OK] Histogram -> {path}"
        return "[FAIL] Could not save"
    except ImportError:
        return "[FAIL] matplotlib not installed"
    except Exception as e:
        return f"[FAIL] {e}"
