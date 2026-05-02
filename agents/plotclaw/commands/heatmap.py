"""Heatmap command - 2D heatmaps"""
import os
from pathlib import Path
name = "heatmap"

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
        return "Usage: /heatmap <row1;row2;row3> [--labels A,B,C] [--ylabels X,Y,Z] [--cmap viridis|magma|plasma|inferno|coolwarm] [--annotate] [--title Title] [--format svg|pdf|png] [--save-only]\nExample: /heatmap 1,2,3;4,5,6;7,8,9 --labels A,B,C --ylabels X,Y,Z --cmap magma --annotate"
    try:
        import matplotlib; matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
        clean_args, flags = parse_flags(args)
        rows = clean_args.split(";")
        data = []
        for row in rows:
            data.append([float(v.strip()) for v in row.split(",")])
        matrix = np.array(data)
        fig, ax = plt.subplots(figsize=(max(6, matrix.shape[1]*1.2), max(5, matrix.shape[0]*1.2)))
        cmap_name = flags.get("cmap", "viridis")
        im = ax.imshow(matrix, cmap=cmap_name, aspect="auto")
        plt.colorbar(im, ax=ax, label="Value")
        if flags.get("annotate"):
            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    ax.text(j, i, f"{matrix[i,j]:.1f}", ha="center", va="center", fontweight="bold")
        xlab = flags.get("labels", "")
        ylab = flags.get("ylabels", "")
        if xlab:
            ax.set_xticks(range(matrix.shape[1]))
            ax.set_xticklabels([l.strip() for l in xlab.split(",")])
        if ylab:
            ax.set_yticks(range(matrix.shape[0]))
            ax.set_yticklabels([l.strip() for l in ylab.split(",")])
        ax.set_title(flags.get("title", "Heatmap"), fontsize=14, fontweight="bold")
        fmt = flags.get("format", "png").lower().strip(".")
        ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
        path = ed / f"heatmap_{hash(str(data))%100000}.{fmt}"
        plt.savefig(str(path), dpi=150, bbox_inches="tight")
        plt.close()
        if os.path.exists(str(path)):
            if not flags.get("save-only"): os.startfile(str(path))
            return f"[OK] Heatmap -> {path}"
        return "[FAIL] Could not save"
    except ImportError:
        return "[FAIL] matplotlib/numpy not installed"
    except Exception as e:
        return f"[FAIL] {e}"
