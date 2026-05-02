"""Heatmap command - Constitutional contract + CLI compatibility"""
import os
from pathlib import Path
name = "heatmap"

def cli_to_payload(args: str) -> dict:
    payload = {"type": "heatmap", "intent": "generate_chart", "task_type": "code_generation", "confidence": 1.0, "source": "user", "flags": {}}
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
                elif key == "labels":
                    payload["xlabels"] = [l.strip() for l in val.split(",")]
                elif key == "ylabels":
                    payload["ylabels"] = [l.strip() for l in val.split(",")]
                else:
                    payload["flags"][key] = val
                i += 2
            else:
                payload["flags"][key] = True; i += 1
        else:
            remaining.append(parts[i]); i += 1
    clean = " ".join(remaining)
    rows = clean.split(";")
    matrix = []
    for row in rows:
        matrix.append([float(v.strip()) for v in row.split(",")])
    payload["matrix"] = matrix
    return payload

def execute(payload: dict) -> str:
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    flags = payload.get("flags", {})
    matrix = np.array(payload.get("matrix", [[0]]))
    fig, ax = plt.subplots(figsize=flags.get("figsize", [max(6, matrix.shape[1]*1.2), max(5, matrix.shape[0]*1.2)]))
    cmap_name = flags.get("cmap", "viridis")
    im = ax.imshow(matrix, cmap=cmap_name, aspect="auto")
    plt.colorbar(im, ax=ax, label="Value")
    if flags.get("annotate"):
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                ax.text(j, i, f"{matrix[i,j]:.1f}", ha="center", va="center", fontweight="bold")
    xlabels = payload.get("xlabels", [])
    ylabels = payload.get("ylabels", [])
    if xlabels:
        ax.set_xticks(range(matrix.shape[1]))
        ax.set_xticklabels(xlabels[:matrix.shape[1]])
    if ylabels:
        ax.set_yticks(range(matrix.shape[0]))
        ax.set_yticklabels(ylabels[:matrix.shape[0]])
    ax.set_title(flags.get("title", "Heatmap"), fontsize=flags.get("fontsize", 11)+3, fontweight="bold")
    fmt = flags.get("format", "png")
    ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
    path = ed / f"heatmap_{hash(str(matrix.tolist()))%100000}.{fmt}"
    fig.savefig(str(path), dpi=flags.get("dpi", 150), bbox_inches="tight")
    plt.close(fig)
    if os.path.exists(str(path)):
        if not (flags.get("save_only") or flags.get("save-only")): os.startfile(str(path))
        return f"[OK] Heatmap -> {path}"
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
            return "Usage: /heatmap <row1;row2;row3> [flags] or pass structured dict"
    except ImportError:
        return "[FAIL] matplotlib/numpy not installed"
    except Exception as e:
        return f"[FAIL] {e}"