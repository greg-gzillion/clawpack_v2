"""Plot command - Constitutional contract + CLI compatibility (sympy-only)"""
import os
from pathlib import Path
name = "plot"

def cli_to_payload(args: str) -> dict:
    payload = {"type": "plot", "intent": "generate_chart", "task_type": "code_generation", "confidence": 1.0, "source": "user", "flags": {}}
    remaining = []
    parts = args.split()
    i = 0
    while i < len(parts):
        if parts[i].startswith("--"):
            key = parts[i][2:]
            if i+1 < len(parts) and not parts[i+1].startswith("--"):
                val = parts[i+1]
                if key in ("range", "figsize", "ylim", "xlim"):
                    payload["flags"][key] = [float(v) for v in val.split(",")]
                elif key in ("dpi", "fontsize"):
                    payload["flags"][key] = int(val)
                elif key == "annotate":
                    pa = val.split(",")
                    if len(pa) >= 3:
                        payload["flags"]["annotate"] = {"text": pa[0], "x": float(pa[1]), "y": float(pa[2])}
                else:
                    payload["flags"][key] = val
                i += 2
            else:
                payload["flags"][key] = True; i += 1
        else:
            remaining.append(parts[i]); i += 1
    clean = " ".join(remaining)
    payload["expressions"] = [e.strip() for e in clean.split(",")] if clean else ["sin(x)"]
    return payload

def execute(payload: dict) -> str:
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import sympy as sp
    flags = payload.get("flags", {})
    expressions = payload.get("expressions", ["sin(x)"])
    rng = flags.get("range", [-10, 10])
    x_min, x_max = rng[0], rng[1]
    if flags.get("logx") and x_min <= 0: x_min = 0.01
    if flags.get("logy") and x_min <= 0: x_min = 0.01
    plt.style.use("dark_background" if flags.get("theme")=="dark" else "default")
    fig, ax = plt.subplots(figsize=flags.get("figsize", [10, 6]))
    use_log = flags.get("logx") or flags.get("logy")
    if use_log:
        x = np.logspace(np.log10(max(x_min, 0.01)), np.log10(max(x_max, 0.1)), 2000)
    else:
        x = np.linspace(x_min, x_max, 2000)
    colors = ["steelblue", "coral", "seagreen", "goldenrod", "purple", "cyan"]
    for i, expr in enumerate(expressions):
        expr_clean = expr.replace("^", "**")
        x_sym = sp.Symbol("x")
        y_sym = sp.sympify(expr_clean)
        y = sp.lambdify(x_sym, y_sym, "numpy")(x)
        ax.plot(x, y, linewidth=2, color=colors[i%len(colors)], label=expr)
    if flags.get("legend") or len(expressions) > 1:
        ax.legend(fontsize=10)
    annotate = flags.get("annotate")
    if annotate:
        ax.annotate(annotate["text"], xy=(annotate["x"], annotate["y"]), xytext=(annotate["x"]+0.5, annotate["y"]+0.5), arrowprops=dict(arrowstyle="->", color="red"), fontsize=10, color="red")
    if flags.get("logx"): ax.set_xscale("log")
    if flags.get("logy"): ax.set_yscale("log")
    ax.set_title(flags.get("title", f"Plot: {', '.join(expressions)}"), fontsize=flags.get("fontsize", 11)+3, fontweight="bold")
    ax.set_xlabel(flags.get("xlabel", "x"), fontsize=flags.get("fontsize", 11))
    ax.set_ylabel(flags.get("ylabel", "f(x)"), fontsize=flags.get("fontsize", 11))
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color="gray", linewidth=0.5)
    ax.axvline(x=0, color="gray", linewidth=0.5)
    if flags.get("ylim"): ax.set_ylim(flags["ylim"])
    if flags.get("xlim"): ax.set_xlim(flags["xlim"])
    fmt = flags.get("format", "png")
    ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
    path = ed / f"plot_{hash(str(expressions))%100000}.{fmt}"
    fig.savefig(str(path), dpi=flags.get("dpi", 150), bbox_inches="tight")
    plt.close(fig)
    if os.path.exists(str(path)):
        if not (flags.get("save_only") or flags.get("save-only")): os.startfile(str(path))
        return f"[OK] Plot -> {path}"
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
            return "Usage: /plot <expr> [flags...] or pass structured dict"
    except ImportError:
        return "[FAIL] matplotlib/numpy/sympy not installed"
    except Exception as e:
        return f"[FAIL] {e}"