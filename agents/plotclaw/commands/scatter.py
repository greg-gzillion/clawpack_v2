"""Scatter command - Scatter plots with regression"""
import os
from pathlib import Path

name = "scatter"
description = "Create scatter plot with optional trendline"

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
        return "Usage: /scatter <x1,x2,x3,...> <y1,y2,y3,...> [--trendline] [--title Title] [--xlabel X] [--ylabel Y] [--theme dark] [--format svg|pdf|png] [--save-only]"

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np

        clean_args, flags = parse_flags(args)
        parts = clean_args.split()
        if len(parts) < 2:
            return "Usage: /scatter <x_values> <y_values>
Example: /scatter 1,2,3,4,5 2,4,5,7,8 --trendline"

        x_vals = [float(x.strip()) for x in parts[0].split(',')]
        y_vals = [float(y.strip()) for y in parts[1].split(',')]

        if len(x_vals) != len(y_vals):
            return "[FAIL] X and Y must have same number of values"

        if flags.get("theme") == "dark":
            plt.style.use('dark_background')
        else:
            plt.style.use('default')

        fig, ax = plt.subplots(figsize=(9, 6))
        ax.scatter(x_vals, y_vals, c='steelblue', s=80, alpha=0.7, edgecolors='black' if flags.get("theme")!="dark" else 'white', linewidth=0.5)

        # Trendline
        if flags.get("trendline"):
            z = np.polyfit(x_vals, y_vals, 1)
            p = np.poly1d(z)
            x_line = np.linspace(min(x_vals), max(x_vals), 100)
            ax.plot(x_line, p(x_line), "r--", linewidth=1.5, label=f"y={z[0]:.2f}x+{z[1]:.2f}")
            ax.legend()

        ax.set_title(flags.get("title", "Scatter Plot"), fontsize=14, fontweight='bold')
        ax.set_xlabel(flags.get("xlabel", "X"), fontsize=11)
        ax.set_ylabel(flags.get("ylabel", "Y"), fontsize=11)
        ax.grid(True, alpha=0.3)

        fmt = flags.get("format", "png").lower().strip(".")
        agent_dir = Path(__file__).parent.parent
        exports_dir = agent_dir / "exports"
        exports_dir.mkdir(exist_ok=True)
        path = exports_dir / f"scatter_{hash(str(x_vals))%100000}.{fmt}"
        plt.savefig(str(path), dpi=150, bbox_inches='tight')
        plt.close()

        if os.path.exists(str(path)):
            if not flags.get("save-only"):
                os.startfile(str(path))
            return f"[OK] Scatter plot saved -> {path}"
        return "[FAIL] Could not save chart"

    except ImportError:
        return "[FAIL] matplotlib/numpy not installed"
    except Exception as e:
        return f"[FAIL] {e}"