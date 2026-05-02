"""Compare command - Constitutional contract + CLI compatibility"""
import os
from pathlib import Path
name = "compare"

def cli_to_payload(args: str) -> dict:
    payload = {"type": "compare", "intent": "generate_chart", "task_type": "code_generation", "confidence": 1.0, "source": "user", "flags": {}, "series": []}
    remaining = []
    parts = args.split()
    i = 0
    while i < len(parts):
        if parts[i].startswith("--"):
            key = parts[i][2:]
            if i+1 < len(parts) and not parts[i+1].startswith("--"):
                val = parts[i+1]
                if key in ("figsize",):
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
    for item in remaining:
        if ":" in item:
            name, vals = item.split(":", 1)
            payload["series"].append({"label": name.strip(), "values": [float(v.strip()) for v in vals.split(",")]})
    return payload

def execute(payload: dict) -> str:
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    flags = payload.get("flags", {})
    series = payload.get("series", [])
    if len(series) < 2:
        return "[FAIL] Need at least 2 datasets"
    plt.style.use("dark_background" if flags.get("theme")=="dark" else "default")
    fig, axes = plt.subplots(1, len(series), figsize=flags.get("figsize", [5*len(series), 5]))
    if len(series) == 1: axes = [axes]
    labels = [f"Item {i+1}" for i in range(len(series[0]["values"]))]
    global_max = max(max(s["values"]) for s in series) * 1.2
    for ax, s in zip(axes, series):
        vals = s["values"]
        colors = plt.cm.viridis(np.linspace(0, 1, len(vals)))
        edge = "white" if flags.get("theme")=="dark" else "black"
        bars = ax.bar(labels, vals, color=colors, edgecolor=edge)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x()+bar.get_width()/2., bar.get_height()+max(vals)*0.01, str(v), ha="center")
        ax.set_title(s["label"], fontweight="bold")
        ax.set_ylim(0, global_max)
    fig.suptitle(flags.get("title", "Comparison"), fontsize=flags.get("fontsize", 11)+3, fontweight="bold")
    plt.tight_layout()
    fmt = flags.get("format", "png")
    ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
    path = ed / f"compare_{hash(str(series))%100000}.{fmt}"
    fig.savefig(str(path), dpi=flags.get("dpi", 150), bbox_inches="tight")
    plt.close(fig)
    if os.path.exists(str(path)):
        if not (flags.get("save_only") or flags.get("save-only")): os.startfile(str(path))
        return f"[OK] Comparison -> {path}"
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
            return "Usage: /compare <A:v1,v2> <B:v1,v2> [flags] or pass structured dict"
    except ImportError:
        return "[FAIL] matplotlib/numpy not installed"
    except Exception as e:
        return f"[FAIL] {e}"