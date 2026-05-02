"""Pie command - Professional pie/donut charts"""
import os
from pathlib import Path

name = "pie"
description = "Create pie or donut charts"

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
        return "Usage: /pie <values> [--labels A,B,C] [--explode 0,0.1,0] [--donut] [--title Title] [--theme dark] [--format svg|pdf|png] [--save-only]
Example: /pie sales:45,costs:30,profit:15 --explode 0,0.1,0 --donut"

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        clean_args, flags = parse_flags(args)

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

        # Parsing from flags
        if flags.get("labels"):
            labels = [l.strip() for l in flags["labels"].split(",")]

        explode_vals = [0] * len(values)
        if flags.get("explode"):
            explode_vals = [float(e.strip()) for e in flags["explode"].split(",")]

        is_donut = bool(flags.get("donut"))

        if flags.get("theme") == "dark":
            plt.style.use('dark_background')
        else:
            plt.style.use('default')

        fig, ax = plt.subplots(figsize=(8, 8))
        colors = plt.cm.Set3(range(len(values)))

        wedges, texts, autotexts = ax.pie(
            values, labels=labels, colors=colors, autopct='%1.1f%%',
            startangle=90, explode=explode_vals,
            pctdistance=0.75 if is_donut else 0.6
        )

        # Donut hole
        if is_donut:
            centre_circle = plt.Circle((0, 0), 0.50, fc='white' if flags.get("theme")!="dark" else '#1e1e1e', edgecolor='none')
            fig.gca().add_artist(centre_circle)

        ax.set_title(flags.get("title", "Pie Chart"), fontsize=14, fontweight='bold')

        fmt = flags.get("format", "png").lower().strip(".")
        agent_dir = Path(__file__).parent.parent
        exports_dir = agent_dir / "exports"
        exports_dir.mkdir(exist_ok=True)
        path = exports_dir / f"pie_{hash(str(values))%100000}.{fmt}"
        plt.savefig(str(path), dpi=150, bbox_inches='tight')
        plt.close()

        if os.path.exists(str(path)):
            if not flags.get("save-only"):
                os.startfile(str(path))
            return f"[OK] Pie chart saved -> {path}"
        return "[FAIL] Could not save chart"

    except ImportError:
        return "[FAIL] matplotlib not installed"
    except Exception as e:
        return f"[FAIL] {e}"