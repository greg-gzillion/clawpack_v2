"""Surface command - Constitutional contract + CLI compatibility"""
import os
from pathlib import Path
name = "surface"

def cli_to_payload(args: str) -> dict:
    payload = {"type": "surface", "intent": "generate_chart", "task_type": "code_generation", "confidence": 1.0, "source": "user", "flags": {}}
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
    payload["expressions"] = [clean] if clean else ["sin(sqrt(x**2+y**2))"]
    return payload

def execute(payload: dict) -> str:
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import sympy as sp
    flags = payload.get("flags", {})
    expr = payload.get("expressions", ["sin(sqrt(x**2+y**2))"])[0]
    rng = flags.get("range", [-5, 5])
    fig = plt.figure(figsize=flags.get("figsize", [10, 8]))
    ax = fig.add_subplot(111, projection="3d")
    x = np.linspace(rng[0], rng[1], 100)
    y = np.linspace(rng[0], rng[1], 100)
    X, Y = np.meshgrid(x, y)
    expr_clean = expr.replace("^", "**")
    x_sym, y_sym = sp.Symbol("x"), sp.Symbol("y")
    z_sym = sp.sympify(expr_clean)
    Z = sp.lambdify((x_sym, y_sym), z_sym, "numpy")(X, Y)
    cmap_name = flags.get("cmap", "viridis")
    surf = ax.plot_surface(X, Y, Z, cmap=cmap_name, edgecolor="none", alpha=0.9)
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=8, label="z")
    ax.set_title(flags.get("title", f"Surface: z = {expr}"), fontsize=flags.get("fontsize", 11)+3, fontweight="bold")
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
    fmt = flags.get("format", "png")
    ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
    path = ed / f"surface_{hash(expr)%100000}.{fmt}"
    fig.savefig(str(path), dpi=flags.get("dpi", 150), bbox_inches="tight")
    plt.close(fig)
    if os.path.exists(str(path)):
        if not (flags.get("save_only") or flags.get("save-only")): os.startfile(str(path))
        return f"[OK] 3D Surface -> {path}"
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
            return "Usage: /surface <z=f(x,y)> [flags] or pass structured dict"
    except ImportError:
        return "[FAIL] matplotlib/numpy/sympy not installed"
    except Exception as e:
        return f"[FAIL] {e}"