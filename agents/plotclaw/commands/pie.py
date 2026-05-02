"""Pie command - Constitutional contract + CLI compatibility"""
import os
from pathlib import Path
name = "pie"

def cli_to_payload(args: str) -> dict:
    from schema import parse_label_values
    payload = {"type": "pie", "intent": "generate_chart", "task_type": "code_generation", "confidence": 1.0, "source": "user", "flags": {}}
    remaining = []
    parts = args.split()
    i = 0
    while i < len(parts):
        if parts[i].startswith("--"):
            key = parts[i][2:]
            if i+1 < len(parts) and not parts[i+1].startswith("--"):
                val = parts[i+1]
                if key == "explode":
                    payload["flags"]["explode"] = [float(v) for v in val.split(",")]
                elif key == "labels":
                    payload["labels"] = [l.strip() for l in val.split(",")]
                else:
                    payload["flags"][key] = val
                i += 2
            else:
                payload["flags"][key] = True; i += 1
        else:
            remaining.append(parts[i]); i += 1
    clean = " ".join(remaining)
    parsed = parse_label_values(clean)
    payload["series"] = [{"label": l, "values": [v]} for l, v in zip(parsed["labels"], parsed["values"])]
    return payload

def execute(payload: dict) -> str:
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    flags = payload.get("flags", {})
    series = payload.get("series", [])
    labels = payload.get("labels", [s["label"] for s in series])
    values = [s["values"][0] for s in series]
    if len(labels) != len(values):
        labels = [f"Item {i+1}" for i in range(len(values))]
    explode_vals = flags.get("explode", [0]*len(values))
    if len(explode_vals) != len(values):
        explode_vals = [0]*len(values)
    is_donut = flags.get("donut") == True
    plt.style.use("dark_background" if flags.get("theme")=="dark" else "default")
    fig, ax = plt.subplots(figsize=flags.get("figsize", [8, 8]))
    colors = plt.cm.Set3(range(len(values)))
    ax.pie(values, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90, explode=explode_vals, pctdistance=0.75 if is_donut else 0.6)
    if is_donut:
        fc = "#1e1e1e" if flags.get("theme")=="dark" else "white"
        fig.gca().add_artist(plt.Circle((0,0), 0.50, fc=fc, edgecolor="none"))
    ax.set_title(flags.get("title", "Pie Chart"), fontsize=flags.get("fontsize", 11)+3, fontweight="bold")
    fmt = flags.get("format", "png")
    ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
    path = ed / f"pie_{hash(str(values))%100000}.{fmt}"
    fig.savefig(str(path), dpi=flags.get("dpi", 150), bbox_inches="tight")
    plt.close(fig)
    if os.path.exists(str(path)):
        if not (flags.get("save_only") or flags.get("save-only")): os.startfile(str(path))
        return f"[OK] Pie chart -> {path}"
    return "[FAIL] Could not save"

def run(args):
    try:
        if isinstance(args, str):
            from schema import validate
            payload = cli_to_payload(args)
            validated = validate(payload)
            if not validated["valid"]: return f"[FAIL] Schema: {validated['error']}"
            return execute(validated["payload"])
        elif isinstance(args, dict):
            from schema import validate
            validated = validate(args)
            if not validated["valid"]: return f"[FAIL] Schema: {validated['error']}"
            return execute(validated["payload"])
        else:
            return "Usage: /pie <values> [flags...] or pass structured dict"
    except ImportError:
        return "[FAIL] matplotlib not installed"
    except Exception as e:
        return f"[FAIL] {e}"