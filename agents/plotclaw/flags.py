"""Universal flag parser - shared across all PlotClaw commands"""
import matplotlib.pyplot as plt

def parse(args):
    """Parse --flag value pairs. Returns (clean_args, flags_dict)."""
    flags = {}
    remaining = []
    parts = args.split()
    i = 0
    while i < len(parts):
        if parts[i].startswith("--"):
            key = parts[i][2:]
            if i + 1 < len(parts) and not parts[i+1].startswith("--"):
                flags[key] = parts[i+1]
                i += 2
            else:
                flags[key] = True
                i += 1
        else:
            remaining.append(parts[i])
            i += 1
    return " ".join(remaining), flags

def apply_style(flags):
    """Apply theme and figure settings from flags. Returns fig, ax."""
    theme = flags.get("theme", "default")
    if theme == "dark":
        plt.style.use("dark_background")
    else:
        plt.style.use("default")
    
    figsize_str = flags.get("figsize", "default")
    if figsize_str != "default" and "," in str(figsize_str):
        try:
            w, h = map(float, str(figsize_str).split(","))
            figsize = (w, h)
        except:
            figsize = (10, 6)
    else:
        figsize = (10, 6)
    
    dpi = int(flags.get("dpi", 150))
    fontsize = int(flags.get("fontsize", 11))
    title_size = int(flags.get("titlesize", 14))
    
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    
    return fig, ax, {
        "fontsize": fontsize,
        "title_size": title_size,
        "dpi": dpi,
        "is_dark": theme == "dark",
    }

def apply_limits(ax, flags):
    """Apply --ylim and --xlim if present."""
    if flags.get("ylim"):
        try:
            lo, hi = map(float, str(flags["ylim"]).split(","))
            ax.set_ylim(lo, hi)
        except:
            pass
    if flags.get("xlim"):
        try:
            lo, hi = map(float, str(flags["xlim"]).split(","))
            ax.set_xlim(lo, hi)
        except:
            pass

def get_edge_color(flags):
    """Return edge color based on theme."""
    return "white" if flags.get("theme") == "dark" else "black"

def get_export_path(name, hash_input, flags):
    """Return export Path object."""
    from pathlib import Path
    fmt = str(flags.get("format", "png")).lower().strip(".")
    ed = Path(__file__).parent / "exports"
    ed.mkdir(exist_ok=True)
    return ed / f"{name}_{hash(str(hash_input))%100000}.{fmt}"

def finish_chart(fig, path, flags):
    """Save, optionally open, and close the figure."""
    import os
    dpi = int(flags.get("dpi", 150))
    plt.tight_layout()
    fig.savefig(str(path), dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    if os.path.exists(str(path)):
        if not flags.get("save-only"):
            os.startfile(str(path))
        return f"[OK] Chart -> {path}"
    return "[FAIL] Could not save"
