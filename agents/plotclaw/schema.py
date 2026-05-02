"""PlotClaw Schema - Constitutional contract for all chart commands.

All chart commands MUST accept this contract.
Constitutional enforcement happens at schema validation,
not scattered across 13 command files.

Principles enforced:
- Audit: structured payload -> deterministic Chronicle logging
- Budget: explicit "type" field for cost classification  
- Truth Resolver: "intent" field for inference tier routing
- Memory Guard: "confidence" field validates persistence eligibility
- Enforcement: schema validation before matplotlib execution
"""

from typing import Dict, List, Union, Optional
from enum import Enum

class ChartType(str, Enum):
    BAR = "bar"
    PIE = "pie"
    PLOT = "plot"
    SCATTER = "scatter"
    HIST = "hist"
    BOX = "box"
    HEATMAP = "heatmap"
    POLAR = "polar"
    SURFACE = "surface"
    COMPARE = "compare"
    ANIMATE = "animate"
    STATS = "stats"
    DASHBOARD = "dashboard"

class ExportFormat(str, Enum):
    PNG = "png"
    SVG = "svg"
    PDF = "pdf"
    GIF = "gif"

# Canonical command payload - the constitutional contract
CANONICAL_PAYLOAD = {
    "type": "bar",                    # ChartType - required
    "intent": "generate_chart",       # For Truth Resolver routing
    "task_type": "code_generation",   # For LLM Router provider selection
    "series": [                       # List of data series
        {
            "label": "Sales",
            "values": [45, 30, 25],
            "errors": None,           # Optional error bars [1.0, 2.0, 0.5]
        }
    ],
    "labels": ["Q1", "Q2", "Q3"],    # Override auto-labels
    "flags": {
        "title": "Chart Title",
        "xlabel": "X Axis",
        "ylabel": "Y Axis",
        "theme": "default",           # "default" | "dark"
        "figsize": [10, 6],          # [width, height]
        "dpi": 150,
        "fontsize": 11,
        "cmap": "viridis",           # Color map
        "colors": None,              # ["red", "blue"] or None
        "format": "png",             # ExportFormat
        "save_only": False,          # Don't open viewer
        "ylim": None,                # [min, max] or None
        "xlim": None,                # [min, max] or None
        "legend": False,
        "annotate": None,            # {"text": "peak", "x": 1.57, "y": 1.0}
        "donut": False,              # Pie-specific
        "explode": None,             # Pie-specific [0, 0.1, 0]
        "horizontal": False,         # Bar-specific
        "stacked": False,            # Bar-specific
        "mean": False,               # Bar-specific
        "std": False,                # Bar-specific
        "trendline": False,          # Scatter-specific
        "bins": 10,                  # Hist-specific
        "logx": False,               # Plot-specific
        "logy": False,               # Plot-specific
        "range": [-10, 10],          # Plot/polar-specific [min, max]
        "frames": 50,                # Animate-specific
        "fps": 10,                   # Animate-specific
        "layout": None,              # Dashboard-specific [rows, cols]
    },
    "confidence": 1.0,               # For Memory Guard persistence check
    "source": "user",                # "user" | "agent" | "csv" | "shared"
}

# CLI label:value parser - preserves backward compatibility
def parse_label_values(args):
    """Parse 'sales:45,costs:30,profit:15' into [{label, values}]."""
    parts = [p.strip() for p in args.split(",") if p.strip()]
    labels, values = [], []
    for p in parts:
        if ":" in p:
            l, v = p.split(":", 1)
            labels.append(l.strip())
            values.append(float(v.strip()))
        else:
            try:
                values.append(float(p))
            except ValueError:
                pass
    if not labels:
        labels = [f"Item {i+1}" for i in range(len(values))]
    return {"labels": labels, "values": values}

def validate(payload: dict) -> dict:
    """Validate a chart payload against the constitutional contract.
    Returns {"valid": True, "payload": payload} or {"valid": False, "error": str}.
    """
    if not isinstance(payload, dict):
        return {"valid": False, "error": "Payload must be a dict"}
    
    if "type" not in payload:
        return {"valid": False, "error": "Missing required field: type"}
    
    chart_type = payload["type"]
    if chart_type not in [e.value for e in ChartType]:
        return {"valid": False, "error": f"Unknown chart type: {chart_type}"}
    
    # Ensure data fields exist for chart types that need them
    data_requirements = {
        "bar": ["series"],
        "pie": ["series"],
        "scatter": ["x_values", "y_values"],
        "hist": ["values"],
        "box": ["datasets"],
        "heatmap": ["matrix"],
        "plot": ["expressions"],
        "polar": ["expressions"],
        "surface": ["expressions"],
        "compare": ["series"],
        "animate": ["expressions"],
        "stats": ["values"],
        "dashboard": ["charts"],
    }
    required = data_requirements.get(chart_type, [])
    for field in required:
        if field not in payload:
            return {"valid": False, "error": f"Chart type {chart_type} requires '{field}'"}
    
    # Constitutional fields
    payload.setdefault("intent", "generate_chart")
    payload.setdefault("task_type", "code_generation")
    payload.setdefault("confidence", 1.0)
    payload.setdefault("source", "user")
    payload.setdefault("flags", {})
    
    # Enforce format
    fmt = payload["flags"].get("format", "png")
    if fmt not in [e.value for e in ExportFormat] and fmt != "gif":
        payload["flags"]["format"] = "png"
    
    return {"valid": True, "payload": payload}