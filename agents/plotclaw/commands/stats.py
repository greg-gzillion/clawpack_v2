"""Stats command - Constitutional contract + CLI compatibility"""
import os
from pathlib import Path
name = "stats"

def cli_to_payload(args: str) -> dict:
    payload = {"type": "stats", "intent": "generate_chart", "task_type": "code_generation", "confidence": 1.0, "source": "user", "flags": {}}
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
    clean = " ".join(remaining)
    payload["values"] = [float(v.strip()) for v in clean.split(",")]
    return payload

def execute(payload: dict) -> str:
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import stats as sp_stats
    flags = payload.get("flags", {})
    arr = np.array(payload.get("values", []))
    plt.style.use("dark_background" if flags.get("theme")=="dark" else "default")
    fig = plt.figure(figsize=flags.get("figsize", [12, 8]))
    edge = "white" if flags.get("theme")=="dark" else "black"
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.hist(arr, bins=min(15, len(set(arr))), color="steelblue", edgecolor=edge, alpha=0.8)
    ax1.axvline(np.mean(arr), color="red", linestyle="--", label=f"Mean: {np.mean(arr):.2f}")
    ax1.axvline(np.median(arr), color="orange", linestyle="--", label=f"Median: {np.median(arr):.2f}")
    ax1.legend(fontsize=8); ax1.set_title("Histogram + Mean/Median", fontweight="bold")
    ax2 = fig.add_subplot(2, 2, 2)
    ax2.boxplot(arr, patch_artist=True); ax2.set_title("Box Plot", fontweight="bold"); ax2.set_xticklabels(["Data"])
    ax3 = fig.add_subplot(2, 2, 3)
    sp_stats.probplot(arr, dist="norm", plot=ax3); ax3.set_title("Q-Q Plot (normality)", fontweight="bold")
    ax3.get_lines()[0].set_markerfacecolor("steelblue"); ax3.get_lines()[0].set_markeredgecolor(edge)
    ax4 = fig.add_subplot(2, 2, 4); ax4.axis("off")
    summary = f"""STATISTICAL SUMMARY
------------------------
Count:    {len(arr)}
Mean:     {np.mean(arr):.4f}
Median:   {np.median(arr):.4f}
Std Dev:  {np.std(arr, ddof=1):.4f}
Variance: {np.var(arr, ddof=1):.4f}
Min:      {np.min(arr):.4f}
Max:      {np.max(arr):.4f}
Range:    {np.max(arr)-np.min(arr):.4f}
Q1 (25%): {np.percentile(arr, 25):.4f}
Q3 (75%): {np.percentile(arr, 75):.4f}
IQR:      {np.percentile(arr,75)-np.percentile(arr,25):.4f}
Skewness: {sp_stats.skew(arr):.4f}
Kurtosis: {sp_stats.kurtosis(arr):.4f}"""
    ax4.text(0.05, 0.95, summary, transform=ax4.transAxes, fontfamily="monospace", fontsize=9, va="top")
    fig.suptitle(flags.get("title", "Statistical Analysis"), fontsize=flags.get("fontsize", 11)+5, fontweight="bold")
    plt.tight_layout()
    fmt = flags.get("format", "png")
    ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
    path = ed / f"stats_{hash(str(arr.tolist()))%100000}.{fmt}"
    fig.savefig(str(path), dpi=flags.get("dpi", 150), bbox_inches="tight")
    plt.close(fig)
    if os.path.exists(str(path)):
        if not (flags.get("save_only") or flags.get("save-only")): os.startfile(str(path))
        return f"[OK] Stats dashboard -> {path}"
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
            return "Usage: /stats <values> [flags] or pass structured dict"
    except ImportError:
        return "[FAIL] matplotlib/numpy/scipy not installed"
    except Exception as e:
        return f"[FAIL] {e}"