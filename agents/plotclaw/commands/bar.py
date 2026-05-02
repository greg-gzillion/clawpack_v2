"""Bar command - Constitutional contract + CLI compatibility"""
import os
from pathlib import Path
name = "bar"

def cli_to_payload(args: str) -> dict:
    """Convert CLI string to constitutional payload."""
    from schema import parse_label_values, CANONICAL_PAYLOAD
    payload = {
        "type": "bar",
        "intent": "generate_chart",
        "task_type": "code_generation",
        "confidence": 1.0,
        "source": "user",
        "flags": {},
    }
    
    # Parse flags
    remaining = []
    parts = args.split()
    i = 0
    while i < len(parts):
        if parts[i].startswith("--"):
            key = parts[i][2:]
            if i + 1 < len(parts) and not parts[i+1].startswith("--"):
                val = parts[i+1]
                if key in ("ylim", "xlim", "figsize", "range"):
                    payload["flags"][key] = [float(v) for v in val.split(",")]
                elif key in ("dpi", "fontsize", "bins", "frames", "fps"):
                    payload["flags"][key] = int(val)
                elif key == "colors":
                    payload["flags"]["colors"] = [c.strip() for c in val.split(",")]
                elif key == "labels":
                    payload["labels"] = [l.strip() for l in val.split(",")]
                elif key == "annotate":
                    parts_a = val.split(",")
                    if len(parts_a) >= 3:
                        payload["flags"]["annotate"] = {"text": parts_a[0], "x": float(parts_a[1]), "y": float(parts_a[2])}
                else:
                    payload["flags"][key] = val
                i += 2
            else:
                payload["flags"][key] = True
                i += 1
        else:
            remaining.append(parts[i])
            i += 1
    
    # Parse values
    clean = " ".join(remaining)
    groups = clean.split()
    
    if len(groups) > 1 and all(":" in g for g in groups):
        # Multi-series stacked
        payload["series"] = []
        for g in groups:
            name, vals = g.split(":", 1)
            payload["series"].append({
                "label": name.strip(),
                "values": [float(v.strip()) for v in vals.split(",")]
            })
        payload["flags"]["stacked"] = True
    else:
        parsed = parse_label_values(clean)
        payload["series"] = [{"label": parsed["labels"][i] if i < len(parsed["labels"]) else f"Item {i+1}", "values": [parsed["values"][i]]} for i in range(len(parsed["values"]))]
        # Flatten for simple bar chart
        payload["series"] = [{"label": l, "values": [v]} for l, v in zip(parsed["labels"], parsed["values"])]
    
    return payload

def execute(payload: dict) -> str:
    """Execute a validated chart payload."""
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    
    flags = payload.get("flags", {})
    series = payload.get("series", [])
    
    plt.style.use("dark_background" if flags.get("theme")=="dark" else "default")
    
    fs = flags.get("figsize", [10, 6])
    dpi_val = flags.get("dpi", 150)
    fig, ax = plt.subplots(figsize=fs)
    
    is_stacked = flags.get("stacked", False)
    is_horizontal = flags.get("horizontal", False)
    
    if is_stacked and len(series) > 1:
        # Stacked bar
        labels = payload.get("labels", [s["label"] for s in series])
        n_items = len(series[0]["values"])
        colors = plt.cm.Set2(range(len(series)))
        edge = "white" if flags.get("theme")=="dark" else "black"
        bottom = np.zeros(n_items)
        for i, s in enumerate(series):
            vals = s["values"]
            ax.bar(range(n_items), vals, bottom=bottom, color=colors[i], label=s["label"], edgecolor=edge, linewidth=0.5)
            bottom += np.array(vals)
        ax.set_xticks(range(n_items))
        ax.set_xticklabels(labels)
        ax.legend()
    else:
        # Simple/flat bar
        labels = [s["label"] for s in series]
        values = [s["values"][0] for s in series]
        n = len(values)
        
        color_list = flags.get("colors")
        if color_list:
            colors = color_list[:n]
        else:
            colors = [plt.cm.viridis(i/max(n-1,1)) for i in range(n)]
        
        edge = "white" if flags.get("theme")=="dark" else "black"
        errors = None
        for s in series:
            if s.get("errors"):
                errors = s["errors"]
                break
        
        if is_horizontal:
            bars = ax.barh(labels, values, color=colors, edgecolor=edge, linewidth=0.8, xerr=errors)
            for bar, v in zip(bars, values):
                ax.text(bar.get_width()+max(values)*0.01, bar.get_y()+bar.get_height()/2., f"{v:.1f}", va="center", fontweight="bold")
            if flags.get("mean"):
                m = np.mean(values)
                ax.axvline(x=m, color="red", linestyle="--", linewidth=1.5, label=f"Mean: {m:.2f}")
                ax.legend()
        else:
            bars = ax.bar(labels, values, color=colors, edgecolor=edge, linewidth=0.8, yerr=errors)
            for bar, v in zip(bars, values):
                ax.text(bar.get_x()+bar.get_width()/2., bar.get_height()+max(values)*0.01, f"{v:.1f}", ha="center", va="bottom", fontweight="bold")
            if flags.get("mean"):
                m = np.mean(values)
                ax.axhline(y=m, color="red", linestyle="--", linewidth=1.5, label=f"Mean: {m:.2f}")
                ax.legend()
            if flags.get("std"):
                m, s = np.mean(values), np.std(values)
                ax.axhspan(m-s, m+s, alpha=0.15, color="blue", label=f"Std: {s:.2f}")
                ax.legend()
            ax.grid(axis="y", alpha=0.3)
    
    ax.set_title(flags.get("title", "Bar Chart"), fontsize=flags.get("fontsize", 11)+3, fontweight="bold")
    ax.set_xlabel(flags.get("xlabel", ""), fontsize=flags.get("fontsize", 11))
    ax.set_ylabel(flags.get("ylabel", "Value"), fontsize=flags.get("fontsize", 11))
    
    if flags.get("ylim"):
        ax.set_ylim(flags["ylim"])
    if flags.get("xlim"):
        ax.set_xlim(flags["xlim"])
    
    fmt = flags.get("format", "png")
    ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
    path = ed / f"bar_{hash(str(values if 'values' in dir() else series))%100000}.{fmt}"
    
    plt.tight_layout()
    fig.savefig(str(path), dpi=dpi_val, bbox_inches="tight")
    plt.close(fig)
    
    if os.path.exists(str(path)):
        if not flags.get("save_only"):
            os.startfile(str(path))
        return f"[OK] Bar chart -> {path}"
    return "[FAIL] Could not save"

def run(args):
    """Accept string (CLI) or dict (A2A contract)."""
    try:
        if isinstance(args, str):
            from schema import validate
            payload = cli_to_payload(args)
            validated = validate(payload)
            if not validated["valid"]:
                return f"[FAIL] Schema validation: {validated['error']}"
            return execute(validated["payload"])
        elif isinstance(args, dict):
            from schema import validate
            validated = validate(args)
            if not validated["valid"]:
                return f"[FAIL] Schema validation: {validated['error']}"
            return execute(validated["payload"])
        else:
            return "Usage: /bar <values> [flags...] or pass structured dict"
    except ImportError:
        return "[FAIL] matplotlib/numpy not installed"
    except Exception as e:
        return f"[FAIL] {e}"