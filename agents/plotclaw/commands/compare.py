"""Compare command - Side-by-side comparison"""
import os
from pathlib import Path
name = "compare"

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
        return "Usage: /compare <A:val1,val2> <B:val1,val2> [--title Title] [--theme dark] [--format svg|pdf|png] [--save-only]\nExample: /compare A:45,30,25 B:35,40,25 --title Q1vsQ2"
    try:
        import matplotlib; matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
        clean_args, flags = parse_flags(args)
        parts = clean_args.split()
        datasets = {}
        for p in parts:
            if ":" in p:
                name, vals = p.split(":", 1)
                datasets[name.strip()] = [float(v.strip()) for v in vals.split(",")]
        if len(datasets) < 2:
            return "[FAIL] Need at least 2 datasets: A:1,2,3 B:4,5,6"
        plt.style.use("dark_background" if flags.get("theme")=="dark" else "default")
        fig, axes = plt.subplots(1, len(datasets), figsize=(5*len(datasets), 5))
        if len(datasets) == 1:
            axes = [axes]
        labels = [f"Item {i+1}" for i in range(len(list(datasets.values())[0]))]
        for ax, (name, values) in zip(axes, datasets.items()):
            colors = plt.cm.viridis(np.linspace(0, 1, len(values)))
            edge = "white" if flags.get("theme")=="dark" else "black"
            bars = ax.bar(labels, values, color=colors, edgecolor=edge)
            for bar, v in zip(bars, values):
                ax.text(bar.get_x()+bar.get_width()/2., bar.get_height()+max(values)*0.01, str(v), ha="center")
            ax.set_title(name, fontweight="bold")
            ax.set_ylim(0, max(list(datasets.values())[0]+list(datasets.values())[1])*1.15)
        fig.suptitle(flags.get("title", "Comparison"), fontsize=14, fontweight="bold")
        plt.tight_layout()
        fmt = flags.get("format", "png").lower().strip(".")
        ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
        path = ed / f"compare_{hash(str(datasets))%100000}.{fmt}"
        plt.savefig(str(path), dpi=150, bbox_inches="tight")
        plt.close()
        if os.path.exists(str(path)):
            if not flags.get("save-only"): os.startfile(str(path))
            return f"[OK] Comparison -> {path}"
        return "[FAIL] Could not save"
    except ImportError:
        return "[FAIL] matplotlib/numpy not installed"
    except Exception as e:
        return f"[FAIL] {e}"
