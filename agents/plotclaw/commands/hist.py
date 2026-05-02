"""Hist command - Constitutional contract + CLI compatibility"""
import os
from pathlib import Path
name = "hist"

def cli_to_payload(args: str) -> dict:
    payload = {"type": "hist", "intent": "generate_chart", "task_type": "code_generation", "confidence": 1.0, "source": "user", "flags": {}}
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
                elif key in ("bins", "dpi", "fontsize"):
                    payload["flags"][key] = int(val)
                else:
                    payload["flags"][key] = val
                i += 2
            else:
                payload["flags"][key] = True; i += 1
        else:
            remaining.append(parts[i]); i += 1
    clean = " ".join(remaining)
    payload["values"] = [float(v.strip()) for v in clean.split(",")]
    return payload

def execute(payload: dict) -> str:
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    flags = payload.get("flags", {})
    values = payload.get("values", [])
    bins = flags.get("bins", 10)
    plt.style.use("dark_background" if flags.get("theme")=="dark" else "default")
    fig, ax = plt.subplots(figsize=flags.get("figsize", [9, 6]))
    edge = "white" if flags.get("theme")=="dark" else "black"
    ax.hist(values, bins=bins, color="steelblue", edgecolor=edge, alpha=0.8)
    ax.set_title(flags.get("title", "Histogram"), fontsize=flags.get("fontsize", 11)+3, fontweight="bold")
    ax.set_xlabel(flags.get("xlabel", "Value"), fontsize=flags.get("fontsize", 11))
    ax.set_ylabel(flags.get("ylabel", "Frequency"), fontsize=flags.get("fontsize", 11))
    ax.grid(axis="y", alpha=0.3)
    if flags.get("ylim"): ax.set_ylim(flags["ylim"])
    if flags.get("xlim"): ax.set_xlim(flags["xlim"])
    fmt = flags.get("format", "png")
    ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
    path = ed / f"hist_{hash(str(values))%100000}.{fmt}"
    fig.savefig(str(path), dpi=flags.get("dpi", 150), bbox_inches="tight")
    plt.close(fig)
    if os.path.exists(str(path)):
        if not (flags.get("save_only") or flags.get("save-only")): os.startfile(str(path))
        return f"[OK] Histogram -> {path}"
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
            return "Usage: /hist <values> [flags] or pass structured dict"
    except ImportError:
        return "[FAIL] matplotlib not installed"
    except Exception as e:
        return f"[FAIL] {e}"