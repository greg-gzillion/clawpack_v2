"""Animate command - Constitutional contract + CLI compatibility"""
import os
from pathlib import Path
name = "animate"

def cli_to_payload(args: str) -> dict:
    payload = {"type": "animate", "intent": "generate_chart", "task_type": "code_generation", "confidence": 1.0, "source": "user", "flags": {}}
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
                elif key in ("frames", "fps", "dpi"):
                    payload["flags"][key] = int(val)
                else:
                    payload["flags"][key] = val
                i += 2
            else:
                payload["flags"][key] = True; i += 1
        else:
            remaining.append(parts[i]); i += 1
    clean = " ".join(remaining)
    payload["expressions"] = [clean] if clean else ["sin(x+t)"]
    return payload

def execute(payload: dict) -> str:
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import sympy as sp
    from matplotlib.animation import FuncAnimation, PillowWriter
    flags = payload.get("flags", {})
    expr = payload.get("expressions", ["sin(x+t)"])[0]
    rng = flags.get("range", [-5, 5])
    frames = flags.get("frames", 50)
    fps = flags.get("fps", 10)
    fig, ax = plt.subplots(figsize=flags.get("figsize", [8, 5]))
    x = np.linspace(rng[0], rng[1], 500)
    line, = ax.plot([], [], linewidth=2, color="steelblue")
    ax.set_xlim(rng[0], rng[1])
    ax.set_ylim(-2, 2)
    ax.grid(True, alpha=0.3)
    def init():
        line.set_data([], []); return line,
    def update(frame):
        t = frame * (6.28 / frames)
        expr_clean = expr.replace("^", "**")
        x_sym, t_sym = sp.Symbol("x"), sp.Symbol("t")
        y_sym = sp.sympify(expr_clean)
        y = sp.lambdify((x_sym, t_sym), y_sym, "numpy")(x, t)
        line.set_data(x, y)
        ax.set_title(f"{flags.get('title', expr)}  t={t:.2f}")
        return line,
    ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True)
    ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
    path = ed / f"animate_{hash(expr)%100000}.gif"
    ani.save(str(path), writer=PillowWriter(fps=fps))
    plt.close(fig)
    if os.path.exists(str(path)):
        if not (flags.get("save_only") or flags.get("save-only")): os.startfile(str(path))
        return f"[OK] Animation ({frames}f, {fps}fps) -> {path}"
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
            return "Usage: /animate <expr(t)> [flags] or pass structured dict"
    except ImportError:
        return "[FAIL] matplotlib/numpy/sympy/Pillow not installed"
    except Exception as e:
        return f"[FAIL] {e}"