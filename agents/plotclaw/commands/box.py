"""Box command - Box and whisker plots"""
import os
from pathlib import Path
name = "box"

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
        return "Usage: /box <series1> <series2> ... [--labels A,B,C] [--title Title] [--horizontal] [--theme dark] [--format svg|pdf|png] [--save-only]\nExample: /box 1,2,3,4,5 2,3,4,5,6 3,4,5,6,7 --labels A,B,C"
    try:
        import matplotlib; matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        clean_args, flags = parse_flags(args)
        parts = clean_args.split()
        datasets = []
        for p in parts:
            datasets.append([float(v.strip()) for v in p.split(",")])
        lab = flags.get("labels", "")
        p_labels = [l.strip() for l in lab.split(",")] if lab else [f"S{i+1}" for i in range(len(datasets))]
        plt.style.use("dark_background" if flags.get("theme")=="dark" else "default")
        fig, ax = plt.subplots(figsize=(max(7, len(datasets)*1.5), 6))
        vert = not flags.get("horizontal")
        bp = ax.boxplot(datasets, labels=p_labels, patch_artist=True, vert=vert)
        colors = plt.cm.Set2(range(len(datasets)))
        for patch, color in zip(bp["boxes"], colors):
            patch.set_facecolor(color)
        ax.set_title(flags.get("title", "Box Plot"), fontsize=14, fontweight="bold")
        ax.grid(axis="y" if vert else "x", alpha=0.3)
        fmt = flags.get("format", "png").lower().strip(".")
        ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
        path = ed / f"box_{hash(str(datasets))%100000}.{fmt}"
        plt.savefig(str(path), dpi=150, bbox_inches="tight")
        plt.close()
        if os.path.exists(str(path)):
            if not flags.get("save-only"): os.startfile(str(path))
            return f"[OK] Box plot -> {path}"
        return "[FAIL] Could not save"
    except ImportError:
        return "[FAIL] matplotlib not installed"
    except Exception as e:
        return f"[FAIL] {e}"
