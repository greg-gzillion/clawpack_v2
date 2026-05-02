"""Scatter command - Constitutional contract + CLI compatibility"""
import os
from pathlib import Path
name = "scatter"

def cli_to_payload(args: str) -> dict:
    payload = {"type": "scatter", "intent": "generate_chart", "task_type": "code_generation", "confidence": 1.0, "source": "user", "flags": {}}
    remaining = []
    parts = args.split()
    i = 0
    while i < len(parts):
        if parts[i].startswith("--"):
            key = parts[i][2:]
            if i+1 < len(parts) and not parts[i+1].startswith("--"):
                val = parts[i+1]
                if key in ("figsize", "ylim", "xlim"):
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
    clean = " ".join(remaining)
    parts2 = clean.split()
    if len(parts2) >= 2:
        payload["x_values"] = [float(v.strip()) for v in parts2[0].split(",")]
        payload["y_values"] = [float(v.strip()) for v in parts2[1].split(",")]
    return payload

def execute(payload: dict) -> str:
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    flags = payload.get("flags", {})
    x_vals = payload.get("x_values", [])
    y_vals = payload.get("y_values", [])
    if len(x_vals) != len(y_vals):
        return "[FAIL] X and Y must have same number of values"
    plt.style.use("dark_background" if flags.get("theme")=="dark" else "default")
    fig, ax = plt.subplots(figsize=flags.get("figsize", [9, 6]))
    edge = "white" if flags.get("theme")=="dark" else "black"
    ax.scatter(x_vals, y_vals, c="steelblue", s=80, alpha=0.7, edgecolors=edge, linewidth=0.5)
    if flags.get("trendline"):
        z = np.polyfit(x_vals, y_vals, 1)
        p = np.poly1d(z)
        x_line = np.linspace(min(x_vals), max(x_vals), 100)
        ax.plot(x_line, p(x_line), "r--", linewidth=1.5, label=f"y={z[0]:.2f}x+{z[1]:.2f}")
        ax.legend()
    ax.set_title(flags.get("title", "Scatter Plot"), fontsize=flags.get("fontsize", 11)+3, fontweight="bold")
    ax.set_xlabel(flags.get("xlabel", "X"), fontsize=flags.get("fontsize", 11))
    ax.set_ylabel(flags.get("ylabel", "Y"), fontsize=flags.get("fontsize", 11))
    ax.grid(True, alpha=0.3)
    if flags.get("ylim"): ax.set_ylim(flags["ylim"])
    if flags.get("xlim"): ax.set_xlim(flags["xlim"])
    fmt = flags.get("format", "png")
    ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
    path = ed / f"scatter_{hash(str(x_vals))%100000}.{fmt}"
    fig.savefig(str(path), dpi=flags.get("dpi", 150), bbox_inches="tight")
    plt.close(fig)
    if os.path.exists(str(path)):
        if not (flags.get("save_only") or flags.get("save-only")): os.startfile(str(path))
        return f"[OK] Scatter -> {path}"
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
            return "Usage: /scatter <x_vals> <y_vals> [flags] or pass structured dict"
    except ImportError:
        return "[FAIL] matplotlib/numpy not installed"
    except Exception as e:
        return f"[FAIL] {e}"