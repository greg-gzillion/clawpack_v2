"""Bar command - Professional bar charts with styling options"""
import os
from pathlib import Path

name = "bar"
description = "Create bar chart with full styling"

def parse_flags(args):
    """Parse --flag value pairs from args string"""
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
        return "Usage: /bar <values> [--labels label1,label2] [--colors red,blue] [--title Title] [--xlabel X] [--ylabel Y] [--mean] [--std] [--theme dark] [--format svg|pdf|png] [--save-only]
Example: /bar sales:45,costs:30,profit:15 --colors red,orange,green --mean"

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np

        clean_args, flags = parse_flags(args)

        # Parse values and optional inline labels
        parts = clean_args.split(",")
        values = []
        labels = []
        for p in parts:
            p = p.strip()
            if ":" in p:
                label, val = p.split(":", 1)
                labels.append(label.strip())
                values.append(float(val.strip()))
            else:
                values.append(float(p))

        if not labels:
            labels = [f"Item {i+1}" for i in range(len(values))]

        # Theme
        if flags.get("theme") == "dark":
            plt.style.use('dark_background')
        else:
            plt.style.use('default')

        fig, ax = plt.subplots(figsize=(max(8, len(values)*1.2), 6))

        # Colors
        color_str = flags.get("colors", "")
        if color_str:
            colors = [c.strip() for c in color_str.split(",")]
        else:
            colors = [plt.cm.viridis(i/max(len(values)-1,1)) for i in range(len(values))]

        bars = ax.bar(labels, values, color=colors, edgecolor='black' if flags.get("theme") != "dark" else 'white', linewidth=0.8)

        # Value labels on bars
        for bar, v in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + max(values)*0.01,
                    f'{v:.1f}', ha='center', va='bottom', fontweight='bold')

        # Statistical overlays
        if "--mean" in flags or flags.get("mean"):
            mean_val = np.mean(values)
            ax.axhline(y=mean_val, color='red', linestyle='--', linewidth=1.5, label=f'Mean: {mean_val:.2f}')
            ax.legend()

        if "--std" in flags or flags.get("std"):
            mean_val = np.mean(values)
            std_val = np.std(values)
            ax.axhspan(mean_val - std_val, mean_val + std_val, alpha=0.15, color='blue', label=f'±1σ: {std_val:.2f}')
            ax.legend()

        # Titles & labels
        ax.set_title(flags.get("title", "Bar Chart"), fontsize=14, fontweight='bold')
        ax.set_xlabel(flags.get("xlabel", ""), fontsize=11)
        ax.set_ylabel(flags.get("ylabel", "Value"), fontsize=11)
        ax.grid(axis='y', alpha=0.3)

        # Export
        fmt = flags.get("format", "png").lower().strip(".")
        agent_dir = Path(__file__).parent.parent
        exports_dir = agent_dir / "exports"
        exports_dir.mkdir(exist_ok=True)

        path = exports_dir / f"bar_{hash(str(values))%100000}.{fmt}"
        plt.savefig(str(path), dpi=150, bbox_inches='tight', facecolor='#1e1e1e' if flags.get("theme")=="dark" else 'white')
        plt.close()

        if os.path.exists(str(path)):
            if not flags.get("save-only"):
                os.startfile(str(path))
            return f"[OK] Bar chart saved -> {path}"
        return "[FAIL] Could not save chart"

    except ImportError:
        return "[FAIL] matplotlib/numpy not installed. Run: pip install matplotlib numpy"
    except Exception as e:
        return f"[FAIL] {e}"