"""Bar command - Professional bar charts"""
import os
from pathlib import Path
name = "bar"

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
        return "Usage: /bar <values> [--labels A,B] [--colors red,blue] [--title T] [--xlabel X] [--ylabel Y] [--mean] [--std] [--horizontal] [--stacked] [--errors 1,2,0.5] [--theme dark] [--format svg|pdf|png] [--save-only]\nMulti-series: /bar sales:45,30,15 costs:20,25,10 --stacked\nExample: /bar sales:45,costs:30,profit:15 --colors red,orange,green --mean --std --theme dark"
    try:
        import matplotlib; matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
        clean_args, flags = parse_flags(args)
        # Check for multi-series (space-separated groups)
        groups = clean_args.split()
        is_multi = len(groups) > 1 and all(":" in g for g in groups)
        
        if is_multi and flags.get("stacked"):
            # Stacked bar chart
            series_data = {}
            for g in groups:
                name, vals = g.split(":", 1)
                series_data[name.strip()] = [float(v.strip()) for v in vals.split(",")]
            series_names = list(series_data.keys())
            n_items = len(list(series_data.values())[0])
            labels = [f"Item {i+1}" for i in range(n_items)]
            if flags.get("labels") and isinstance(flags["labels"], str):
                labels = [l.strip() for l in flags["labels"].split(",")]
            plt.style.use("dark_background" if flags.get("theme")=="dark" else "default")
            fig, ax = plt.subplots(figsize=(max(8, n_items*1.5), 6))
            colors = plt.cm.Set2(range(len(series_names)))
            bottom = np.zeros(n_items)
            for i, name in enumerate(series_names):
                vals = series_data[name]
                ax.bar(labels, vals, bottom=bottom, color=colors[i], label=name, edgecolor="white" if flags.get("theme")=="dark" else "black", linewidth=0.5)
                bottom += np.array(vals)
            ax.legend()
        else:
            # Simple bar chart
            parts = clean_args.split(",")
            values, labels = [], []
            for p in parts:
                p = p.strip()
                if ":" in p:
                    l, v = p.split(":", 1)
                    labels.append(l.strip()); values.append(float(v.strip()))
                else:
                    values.append(float(p))
            if not labels:
                labels = [f"Item {i+1}" for i in range(len(values))]
            if flags.get("labels") and isinstance(flags["labels"], str):
                labels = [l.strip() for l in flags["labels"].split(",")]
            plt.style.use("dark_background" if flags.get("theme")=="dark" else "default")
            n = len(values)
            horizontal = flags.get("horizontal")
            fig, ax = plt.subplots(figsize=(max(8, n*1.2), 6))
            color_str = flags.get("colors", "")
            colors = [c.strip() for c in color_str.split(",")] if color_str else [plt.cm.viridis(i/max(n-1,1)) for i in range(n)]
            edge = "white" if flags.get("theme")=="dark" else "black"
            err_str = flags.get("errors", "")
            errors = [float(e.strip()) for e in err_str.split(",")] if err_str else None
            
            if horizontal:
                bars = ax.barh(labels, values, color=colors, edgecolor=edge, linewidth=0.8, xerr=errors)
                for bar, v in zip(bars, values):
                    ax.text(bar.get_width()+max(values)*0.01, bar.get_y()+bar.get_height()/2., f"{v:.1f}", va="center", fontweight="bold")
                if flags.get("mean"):
                    m = np.mean(values)
                    ax.axvline(x=m, color="red", linestyle="--", linewidth=1.5, label=f"Mean: {m:.2f}")
                    ax.legend()
            else:
                bars = ax.bar(labels, values, color=colors, edgecolor=edge, linewidth=0.8, yerr=errors)
                for bar, v in zip(bars, values):
                    ax.text(bar.get_x()+bar.get_width()/2., bar.get_height()+max(values)*0.01, f"{v:.1f}", ha="center", va="bottom", fontweight="bold")
                if flags.get("mean"):
                    m = np.mean(values)
                    ax.axhline(y=m, color="red", linestyle="--", linewidth=1.5, label=f"Mean: {m:.2f}")
                    ax.legend()
                if flags.get("std"):
                    m, s = np.mean(values), np.std(values)
                    ax.axhspan(m-s, m+s, alpha=0.15, color="blue", label=f"Std: {s:.2f}")
                    ax.legend()
                ax.grid(axis="y", alpha=0.3)
            
            values_for_title = values
        
        ax.set_title(flags.get("title", "Bar Chart"), fontsize=14, fontweight="bold")
        ax.set_xlabel(flags.get("xlabel", ""), fontsize=11)
        ax.set_ylabel(flags.get("ylabel", "Value"), fontsize=11)
        
        fmt = flags.get("format", "png").lower().strip(".")
        ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
        path = ed / f"bar_{hash(str(values_for_title if 'values_for_title' in dir() else ''))%100000}.{fmt}"
        plt.savefig(str(path), dpi=150, bbox_inches="tight")
        plt.close()
        if os.path.exists(str(path)):
            if not flags.get("save-only"): os.startfile(str(path))
            return f"[OK] Bar chart -> {path}"
        return "[FAIL] Could not save"
    except ImportError:
        return "[FAIL] matplotlib/numpy not installed"
    except Exception as e:
        return f"[FAIL] {e}"
