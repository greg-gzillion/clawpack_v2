"""Stats command - Auto-generate histogram + box + summary"""
import os
from pathlib import Path
name = "stats"

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
        return "Usage: /stats <values> [--title Title] [--theme dark] [--format svg|pdf|png] [--save-only]\nExample: /stats 1,2,2,3,3,3,4,4,4,4,5,5,5,5,5"
    try:
        import matplotlib; matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
        from scipy import stats as sp_stats
        clean_args, flags = parse_flags(args)
        values = [float(v.strip()) for v in clean_args.split(",")]
        arr = np.array(values)
        plt.style.use("dark_background" if flags.get("theme")=="dark" else "default")
        fig = plt.figure(figsize=(12, 8))
        # Histogram
        ax1 = fig.add_subplot(2, 2, 1)
        edge = "white" if flags.get("theme")=="dark" else "black"
        ax1.hist(arr, bins=min(15, len(set(values))), color="steelblue", edgecolor=edge, alpha=0.8)
        ax1.axvline(np.mean(arr), color="red", linestyle="--", label=f"Mean: {np.mean(arr):.2f}")
        ax1.axvline(np.median(arr), color="orange", linestyle="--", label=f"Median: {np.median(arr):.2f}")
        ax1.legend(fontsize=8)
        ax1.set_title("Histogram + Mean/Median", fontweight="bold")
        # Box plot
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.boxplot(arr, patch_artist=True)
        ax2.set_title("Box Plot", fontweight="bold")
        ax2.set_xticklabels(["Data"])
        # QQ plot
        ax3 = fig.add_subplot(2, 2, 3)
        sp_stats.probplot(arr, dist="norm", plot=ax3)
        ax3.set_title("Q-Q Plot (normality)", fontweight="bold")
        ax3.get_lines()[0].set_markerfacecolor("steelblue")
        ax3.get_lines()[0].set_markeredgecolor(edge)
        # Summary text
        ax4 = fig.add_subplot(2, 2, 4)
        ax4.axis("off")
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
        fig.suptitle(flags.get("title", "Statistical Analysis"), fontsize=16, fontweight="bold")
        plt.tight_layout()
        fmt = flags.get("format", "png").lower().strip(".")
        ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
        path = ed / f"stats_{hash(str(values))%100000}.{fmt}"
        plt.savefig(str(path), dpi=150, bbox_inches="tight")
        plt.close()
        if os.path.exists(str(path)):
            if not flags.get("save-only"): os.startfile(str(path))
            return f"[OK] Stats dashboard -> {path}"
        return "[FAIL] Could not save"
    except ImportError as e:
        return f"[FAIL] Missing dependency: {e}. Run: pip install matplotlib numpy scipy pillow"
    except Exception as e:
        return f"[FAIL] {e}"
