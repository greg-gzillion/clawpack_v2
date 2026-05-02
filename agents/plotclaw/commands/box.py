"""Box command - Constitutional contract + CLI compatibility"""
import os
from pathlib import Path
name = "box"

def cli_to_payload(args: str) -> dict:
    payload = {"type": "box", "intent": "generate_chart", "task_type": "code_generation", "confidence": 1.0, "source": "user", "flags": {}}
    remaining = []
    parts = args.split()
    i = 0
    while i < len(parts):
        if parts[i].startswith("--"):
            key = parts[i][2:]
            if i+1 < len(parts) and not parts[i+1].startswith("--"):
                val = parts[i+1]
                if key in ("figsize", "ylim"):
                    payload["flags"][key] = [float(v) for v in val.split(",")]
                elif key in ("dpi", "fontsize"):
                    payload["flags"][key] = int(val)
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
    # Each space-separated group is a dataset
    for group in clean.split():
        vals = [float(v.strip()) for v in group.split(",")]
        if vals:
            payload.setdefault("datasets", []).append(vals)
    return payload

def execute(payload: dict) -> str:
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    flags = payload.get("flags", {})
    datasets = payload.get("datasets", [])
    labels = payload.get("labels", [f"S{i+1}" for i in range(len(datasets))])
    plt.style.use("dark_background" if flags.get("theme")=="dark" else "default")
    fig, ax = plt.subplots(figsize=flags.get("figsize", [max(7, len(datasets)*1.5), 6]))
    vert = not flags.get("horizontal")
    bp = ax.boxplot(datasets, labels=labels, patch_artist=True, vert=vert)
    colors = plt.cm.Set2(range(len(datasets)))
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
    ax.set_title(flags.get("title", "Box Plot"), fontsize=flags.get("fontsize", 11)+3, fontweight="bold")
    ax.grid(axis="y" if vert else "x", alpha=0.3)
    if flags.get("ylim"): ax.set_ylim(flags["ylim"])
    fmt = flags.get("format", "png")
    ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
    path = ed / f"box_{hash(str(datasets))%100000}.{fmt}"
    fig.savefig(str(path), dpi=flags.get("dpi", 150), bbox_inches="tight")
    plt.close(fig)
    if os.path.exists(str(path)):
        if not (flags.get("save_only") or flags.get("save-only")): os.startfile(str(path))
        return f"[OK] Box plot -> {path}"
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
            return "Usage: /box <dataset1> <dataset2> ... [flags] or pass structured dict"
    except ImportError:
        return "[FAIL] matplotlib not installed"
    except Exception as e:
        return f"[FAIL] {e}"