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
import re

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
    "type": "bar",
    "intent": "generate_chart",
    "task_type": "code_generation",
    "series": [
        {
            "label": "Sales",
            "values": [45, 30, 25],
            "errors": None,
        }
    ],
    "labels": ["Q1", "Q2", "Q3"],
    "flags": {
        "title": "Chart Title",
        "xlabel": "X Axis",
        "ylabel": "Y Axis",
        "theme": "default",
        "figsize": [10, 6],
        "dpi": 150,
        "fontsize": 11,
        "cmap": "viridis",
        "colors": None,
        "format": "png",
        "save_only": False,
        "ylim": None,
        "xlim": None,
        "legend": False,
        "annotate": None,
        "donut": False,
        "explode": None,
        "horizontal": False,
        "stacked": False,
        "mean": False,
        "std": False,
        "trendline": False,
        "bins": 10,
        "logx": False,
        "logy": False,
        "range": [-10, 10],
        "frames": 50,
        "fps": 10,
        "layout": None,
    },
    "confidence": 1.0,
    "source": "user",
}


def _clean_value(token: str) -> str:
    """Strip currency symbols, commas, and expand K/M suffixes."""
    token = token.strip()
    token = token.replace("$", "").replace(",", "").replace("%", "")
    token = re.sub(r'(\d+\.?\d*)\s*K', lambda m: str(int(float(m.group(1)) * 1000)), token, flags=re.IGNORECASE)
    token = re.sub(r'(\d+\.?\d*)\s*M', lambda m: str(int(float(m.group(1)) * 1000000)), token, flags=re.IGNORECASE)
    return token


def parse_label_values(args: str) -> dict:
    """Parse various input formats into {labels, values}.

    Handles:
      - Space-separated pairs: "Q1 45 Q2 62 Q3 58 Q4 71"
      - Comma-separated label:value: "sales:45,costs:30,profit:15"
      - Raw numbers: "45,62,58,71"
      - Currency/K/M suffixes: ", , " -> [45000, 62000, 58000]
    """
    args = args.strip()
    if not args:
        return {"labels": [], "values": []}

    # Try space-separated pairs: "Q1 45 Q2 62 Q3 58 Q4 71"
    tokens = args.split()
    if len(tokens) >= 2:
        cleaned = [_clean_value(t) for t in tokens]
        # Check alternating label/number pattern
        is_pairs = True
        for i, t in enumerate(cleaned):
            if i % 2 == 0:
                if t.replace('.', '').replace('-', '').isdigit():
                    is_pairs = False
                    break
            else:
                if not t.replace('.', '').replace('-', '').lstrip('-').isdigit():
                    is_pairs = False
                    break
        if is_pairs and len(cleaned) % 2 == 0:
            labels = [tokens[i] for i in range(0, len(tokens), 2)]
            values = [float(cleaned[i]) for i in range(1, len(tokens), 2)]
            return {"labels": labels, "values": values}

    # Comma-separated: "sales:45,costs:30" or "45,62,58"
    parts = [p.strip() for p in args.split(",") if p.strip()]
    labels, values = [], []
    for p in parts:
        if ":" in p:
            l, v = p.split(":", 1)
            labels.append(l.strip())
            values.append(float(_clean_value(v)))
        else:
            try:
                values.append(float(_clean_value(p)))
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

    payload.setdefault("intent", "generate_chart")
    payload.setdefault("task_type", "code_generation")
    payload.setdefault("confidence", 1.0)
    payload.setdefault("source", "user")
    payload.setdefault("flags", {})

    fmt = payload["flags"].get("format", "png")
    if fmt not in [e.value for e in ExportFormat] and fmt != "gif":
        payload["flags"]["format"] = "png"

    return {"valid": True, "payload": payload}
