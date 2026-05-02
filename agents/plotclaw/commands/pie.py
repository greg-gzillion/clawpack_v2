"""Pie command - Professional pie/donut charts"""
import os
from pathlib import Path
name = "pie"

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
        return "Usage: /pie <values> [--labels A,B,C] [--explode 0,0.1,0] [--donut] [--title Title] [--theme dark] [--format svg|pdf|png] [--save-only]\nExample: /pie market:40,30,20,10 --explode 0,0.1,0,0 --donut --theme dark"
    try:
        import matplotlib; matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        clean_args, flags = parse_flags(args)
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
        # Flag labels override
        if flags.get("labels") and isinstance(flags["labels"], str):
            labels = [l.strip() for l in flags["labels"].split(",")]
        # Explode
        if flags.get("explode") and isinstance(flags["explode"], str):
            explode_vals = [float(e.strip()) for e in flags["explode"].split(",")]
        else:
            explode_vals = [0] * len(values)
        is_donut = flags.get("donut") == True
        plt.style.use("dark_background" if flags.get("theme")=="dark" else "default")
        fig, ax = plt.subplots(figsize=(8, 8))
        colors = plt.cm.Set3(range(len(values)))
        wedges, texts, autotexts = ax.pie(values, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90, explode=explode_vals, pctdistance=0.75 if is_donut else 0.6)
        if is_donut:
            fc = "#1e1e1e" if flags.get("theme")=="dark" else "white"
            centre_circle = plt.Circle((0, 0), 0.50, fc=fc, edgecolor="none")
            fig.gca().add_artist(centre_circle)
        ax.set_title(flags.get("title", "Pie Chart"), fontsize=14, fontweight="bold")
        fmt = flags.get("format", "png").lower().strip(".")
        ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
        path = ed / f"pie_{hash(str(values))%100000}.{fmt}"
        plt.savefig(str(path), dpi=150, bbox_inches="tight")
        plt.close()
        if os.path.exists(str(path)):
            if not flags.get("save-only"): os.startfile(str(path))
            return f"[OK] Pie chart -> {path}"
        return "[FAIL] Could not save"
    except ImportError:
        return "[FAIL] matplotlib not installed"
    except Exception as e:
        return f"[FAIL] {e}"
