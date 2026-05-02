"""Animate command - Save animated GIF"""
import os
from pathlib import Path
name = "animate"

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
        return "Usage: /animate <expr(t)> [--range 0,6.28] [--frames 50] [--fps 10] [--title Title] [--save-only]\nExample: /animate sin(x+t) --range 0,6.28 --frames 60 --fps 15"
    try:
        import matplotlib; matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
        from matplotlib.animation import FuncAnimation, PillowWriter
        clean_args, flags = parse_flags(args)
        expr = clean_args.split()[0] if clean_args else "sin(x+t)"
        rng = flags.get("range", "-5,5")
        x_min, x_max = map(float, rng.split(","))
        frames = int(flags.get("frames", 50))
        fps = int(flags.get("fps", 10))
        fig, ax = plt.subplots(figsize=(8, 5))
        x = np.linspace(x_min, x_max, 500)
        line, = ax.plot([], [], linewidth=2, color="steelblue")
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(-2, 2)
        ax.grid(True, alpha=0.3)
        ax.set_title(flags.get("title", f"Animation: {expr}"))
        def init():
            line.set_data([], [])
            return line,
        def update(frame):
            t = frame * (6.28 / frames)
            ns = {"x": x, "t": t, "np": np, "sin": np.sin, "cos": np.cos, "exp": np.exp, "pi": np.pi}
            y = eval(expr.replace("^","**"), {"__builtins__": {}}, ns)
            line.set_data(x, y)
            ax.set_title(f"{flags.get('title', expr)}  t={t:.2f}")
            return line,
        ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True)
        ed = Path(__file__).parent.parent / "exports"; ed.mkdir(exist_ok=True)
        path = ed / f"animate_{hash(expr)%100000}.gif"
        ani.save(str(path), writer=PillowWriter(fps=fps))
        plt.close()
        if os.path.exists(str(path)):
            if not flags.get("save-only"): os.startfile(str(path))
            return f"[OK] Animation ({frames}frames, {fps}fps) -> {path}"
        return "[FAIL] Could not save"
    except ImportError:
        return "[FAIL] matplotlib/numpy/Pillow not installed. Run: pip install pillow"
    except Exception as e:
        return f"[FAIL] {e}"
