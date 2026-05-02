"""Dashboard command - Constitutional contract + CLI compatibility"""
import os
from pathlib import Path
name = "dashboard"

def cli_to_payload(args: str) -> dict:
    payload = {"type": "dashboard", "intent": "generate_chart", "task_type": "code_generation", "confidence": 1.0, "source": "user", "flags": {}, "charts": []}
    remaining = []
    parts = args.split()
    i = 0
    while i < len(parts):
        if parts[i].startswith("--"):
            key = parts[i][2:]
            if i+1 < len(parts) and not parts[i+1].startswith("--"):
                val = parts[i+1]
                if key in ("layout",):
                    payload["flags"]["layout"] = [int(v) for v in val.split(",")]
                elif key in ("figsize",):
                    payload["flags"][key] = [float(v) for v in val.split(",")]
                elif key in ("dpi", "fontsize"):
                    payload["flags"][key] = int(val)
                else:
                    payload["flags"][key] = val
                i += 2
            else:
                payload["flags"][key] = True; i += 1
        else:
            remaining.append(parts[i]); i += 1
    for raw in remaining:
        pts = raw.split(":")
        if len(pts) >= 3:
            payload["charts"].append({
                "type": pts[0],
                "label": pts[1],
                "values": [float(v) for v in pts[2].split(",")]
            })
    return payload

def execute(payload: dict) -> str:
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    flags = payload.get("flags", {})
    charts = payload.get("charts", [])
    if not charts:
        return "[FAIL] No valid charts"
    n = len(charts)
    layout = flags.get("layout")
    if layout: rows, cols = layout[0], layout[1]
    else: cols = min(n, 3); rows = (n + cols - 1) // cols
    plt.style.use("dark_background" if flags.get("theme")=="dark" else "default")
    fig, axes = plt.subplots(rows, cols, figsize=flags.get("figsize", [6*cols, 5*rows]))
    if n == 1: axes = [axes]
    else: axes = axes.flatten() if hasattr(axes, "flatten") else [axes]
    for i, ch in enumerate(charts):
        ax = axes[i]; ctype = ch["type"]; label = ch["label"]; values = ch["values"]
        labels = [f"{label}{j+1}" for j in range(len(values))]
        if ctype == "bar":
            colors = plt.cm.viridis(np.linspace(0, 1, len(values)))
            edge = "white" if flags.get("theme")=="dark" else "black"
            ax.bar(labels, values, color=colors, edgecolor=edge)
            for bar, v in zip(ax.patches, values):
                ax.text(bar.get_x()+bar.get_width()/2., bar.get_height()+max(values)*0.01, str(v), ha="center")
        elif ctype == "pie":
            colors = plt.cm.Set3(range(len(values)))
            ax.pie(values, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
        elif ctype == "line":
            x = range(len(values))
            ax.plot(x, values, "o-", linewidth=2, color="steelblue", markersize=8)
            ax.set_xticks(x); ax.set_xticklabels(labels)
        ax.set_title(label, fontsize=flags.get("fontsize", 11), fontweight="bold")
    for j in range(i+1, len(axes)): axes[j].set_visible(False)
    fig.suptitle(flags.get("title", "Dashboard"), fontsize=flags.get("fontsize", 11)+3, fontweight="bold")
    plt.tight_layout()
    fmt = flags.get("format", "png")
    ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
    path = ed / f"dashboard_{hash(str(charts))%100000}.{fmt}"
    fig.savefig(str(path), dpi=flags.get("dpi", 150), bbox_inches="tight")
    plt.close(fig)
    if os.path.exists(str(path)):
        if not (flags.get("save_only") or flags.get("save-only")): os.startfile(str(path))
        return f"[OK] Dashboard -> {path}"
    return "[FAIL] Could not save"

def run(args):
    try:
        if isinstance(args, str):
            from agents.plotclaw.schema import validate
            payload = cli_to_payload(args)
            validated = validate(payload)
            if not validated["valid"]: return f"[FAIL] Schema: {validated['error']}"
            return execute(validated["payload"])
        elif isinstance(args, dict):
            from agents.plotclaw.schema import validate
            validated = validate(args)
            if not validated["valid"]: return f"[FAIL] Schema: {validated['error']}"
            return execute(validated["payload"])
        else:
            return "Usage: /dashboard <type:label:v1,v2> ... [flags] or pass structured dict"
    except ImportError:
        return "[FAIL] matplotlib/numpy not installed"
    except Exception as e:
        return f"[FAIL] {e}"