"""Dashboard command - Multiple charts in one view"""
import os
from pathlib import Path

name = "dashboard"
description = "Create multi-chart dashboard"

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
        return 'Usage: /dashboard <chart1:values> <chart2:values> ... [--title Title] [--layout rows,cols] [--theme dark]
Each chart: type:label1:val1,label2:val2,...
Types: bar, pie, line
Example: /dashboard bar:sales:45,costs:30,profit:15 pie:market:40,30,20,10 line:growth:1,2,4,8,16'

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np

        clean_args, flags = parse_flags(args)
        charts_raw = clean_args.split()

        chart_specs = []
        for raw in charts_raw:
            parts = raw.split(":")
            if len(parts) >= 3:
                chart_type = parts[0]
                chart_label = parts[1]
                values = [float(v) for v in parts[2].split(",")]
                labels = [f"{chart_label}{i+1}" for i in range(len(values))]
                chart_specs.append((chart_type, chart_label, values, labels))

        if not chart_specs:
            return "[FAIL] No valid chart specs. Use: bar:name:val1,val2 pie:name:val1,val2"

        n = len(chart_specs)
        layout = flags.get("layout", "")
        if layout:
            rows, cols = map(int, layout.split(","))
        else:
            cols = min(n, 3)
            rows = (n + cols - 1) // cols

        if flags.get("theme") == "dark":
            plt.style.use('dark_background')
        else:
            plt.style.use('default')

        fig, axes = plt.subplots(rows, cols, figsize=(6*cols, 5*rows))
        if n == 1:
            axes = [axes]
        else:
            axes = axes.flatten() if hasattr(axes, 'flatten') else [axes]

        for i, (chart_type, label, values, labels) in enumerate(chart_specs):
            ax = axes[i]
            if chart_type == "bar":
                colors = plt.cm.viridis(np.linspace(0, 1, len(values)))
                ax.bar(labels, values, color=colors, edgecolor='black' if flags.get("theme")!="dark" else 'white')
                for bar, v in zip(ax.patches, values):
                    ax.text(bar.get_x()+bar.get_width()/2., bar.get_height()+max(values)*0.01, str(v), ha='center')
            elif chart_type == "pie":
                colors = plt.cm.Set3(range(len(values)))
                ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            elif chart_type == "line":
                x = range(len(values))
                ax.plot(x, values, 'o-', linewidth=2, color='steelblue', markersize=8)
                ax.set_xticks(x)
                ax.set_xticklabels(labels)
            ax.set_title(f"{label}", fontsize=12, fontweight='bold')

        # Hide unused subplots
        for j in range(i+1, len(axes)):
            axes[j].set_visible(False)

        fig.suptitle(flags.get("title", "Dashboard"), fontsize=16, fontweight='bold')
        plt.tight_layout()

        fmt = flags.get("format", "png").lower().strip(".")
        agent_dir = Path(__file__).parent.parent
        exports_dir = agent_dir / "exports"
        exports_dir.mkdir(exist_ok=True)
        path = exports_dir / f"dashboard_{hash(str(chart_specs))%100000}.{fmt}"
        plt.savefig(str(path), dpi=150, bbox_inches='tight')
        plt.close()

        if os.path.exists(str(path)):
            if not flags.get("save-only"):
                os.startfile(str(path))
            return f"[OK] Dashboard saved -> {path}"
        return "[FAIL] Could not save dashboard"

    except ImportError:
        return "[FAIL] matplotlib/numpy not installed"
    except Exception as e:
        return f"[FAIL] {e}"