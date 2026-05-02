"""Polar command - Constitutional contract + CLI compatibility"""
import os
from pathlib import Path
name = "polar"

def cli_to_payload(args: str) -> dict:
    payload = {"type": "polar", "intent": "generate_chart", "task_type": "code_generation", "confidence": 1.0, "source": "user", "flags": {}}
    remaining = []
    parts = args.split()
    i = 0
    while i < len(parts):
        if parts[i].startswith("--"):
            key = parts[i][2:]
            if i+1 < len(parts) and not parts[i+1].startswith("--"):
                val = parts[i+1]
                if key in ("range", "figsize"):
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
    payload["expressions"] = [clean] if clean else ["sin(2*theta)"]
    return payload

def execute(payload: dict) -> str:
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import sympy as sp
    flags = payload.get("flags", {})
    expr = payload.get("expressions", ["sin(2*theta)"])[0]
    rng = flags.get("range", [0, 6.28])
    plt.style.use("dark_background" if flags.get("theme")=="dark" else "default")
    theta = np.linspace(rng[0], rng[1], 1000)
    expr_clean = expr.replace("^", "**")
    t_sym = sp.Symbol("theta")
    r_sym = sp.sympify(expr_clean)
    r = sp.lambdify(t_sym, r_sym, "numpy")(theta)
    fig, ax = plt.subplots(figsize=flags.get("figsize", [8, 8]), subplot_kw={"projection": "polar"})
    ax.plot(theta, r, linewidth=2, color="steelblue")
    ax.fill(theta, r, alpha=0.2, color="steelblue")
    ax.set_title(flags.get("title", f"Polar: r = {expr}"), fontsize=flags.get("fontsize", 11)+3, fontweight="bold", pad=20)
    ax.grid(True)
    fmt = flags.get("format", "png")
    ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
    path = ed / f"polar_{hash(expr)%100000}.{fmt}"
    fig.savefig(str(path), dpi=flags.get("dpi", 150), bbox_inches="tight")
    plt.close(fig)
    if os.path.exists(str(path)):
        if not (flags.get("save_only") or flags.get("save-only")): os.startfile(str(path))
        return f"[OK] Polar -> {path}"
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
            return "Usage: /polar <r(theta)> [flags] or pass structured dict"
    except ImportError:
        return "[FAIL] matplotlib/numpy/sympy not installed"
    except Exception as e:
        return f"[FAIL] {e}"