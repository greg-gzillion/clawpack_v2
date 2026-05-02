"""FlowClaw Schema - Constitutional contract for diagram generation.

All FlowClaw commands MUST accept this contract.
Schema validation before any diagram engine execution.
"""
from typing import Dict, List, Optional
from enum import Enum

class DiagramType(str, Enum):
    FLOWCHART = "flowchart"
    SEQUENCE = "sequence"
    ARCHITECTURE = "architecture"
    MINDMAP = "mindmap"
    GANTT = "gantt"

class ExportFormat(str, Enum):
    PNG = "png"
    SVG = "svg"
    PDF = "pdf"
    DOCX = "docx"
    MD = "md"
    HTML = "html"
    MMD = "mmd"

CANONICAL_PAYLOAD = {
    "type": "diagram",                  # Always "diagram"
    "diagram_type": "flowchart",        # DiagramType
    "intent": "generate_diagram",       # For Truth Resolver
    "task_type": "code_generation",     # For LLM Router
    "confidence": 1.0,                  # For Memory Guard
    "source": "user",                   # "user" | "agent" | "shared"
    "query": "User login flow",         # Description
    "context": {},                      # Optional: {"webclaw": "...", "dataclaw": "..."}
    "flags": {
        "view": False,                  # Open in browser
        "export_format": "md",          # ExportFormat
        "save_only": False,             # Don't open viewer
        "title": "",                    # Diagram title
        "theme": "default",             # "default" | "dark" | "neutral"
    },
    "delegate": {                       # Cross-agent delegation
        "target_agent": None,           # e.g. "plotclaw", "interpretclaw"
        "command": None,                # Task for target agent
        "payload": None,                # Structured payload for target
    }
}

def validate(payload: dict) -> dict:
    """Validate a FlowClaw payload against the constitutional contract."""
    if not isinstance(payload, dict):
        return {"valid": False, "error": "Payload must be a dict"}
    
    if "type" not in payload:
        payload["type"] = "diagram"
    
    if payload.get("type") == "delegate":
        if "target_agent" not in payload:
            return {"valid": False, "error": "Delegate requires target_agent"}
        payload.setdefault("intent", "agent_delegation")
        payload.setdefault("confidence", 1.0)
        return {"valid": True, "payload": payload}
    
    if payload.get("type") != "diagram":
        return {"valid": False, "error": f"Unknown type: {payload.get('type')}"}
    
    diag_type = payload.get("diagram_type", "flowchart")
    if diag_type not in [e.value for e in DiagramType]:
        payload["diagram_type"] = "flowchart"
    
    payload.setdefault("intent", "generate_diagram")
    payload.setdefault("task_type", "code_generation")
    payload.setdefault("confidence", 1.0)
    payload.setdefault("source", "user")
    payload.setdefault("query", "")
    payload.setdefault("flags", {})
    payload.setdefault("context", {})
    payload.setdefault("delegate", {})
    
    fmt = payload["flags"].get("export_format", "md")
    if fmt not in [e.value for e in ExportFormat]:
        payload["flags"]["export_format"] = "md"
    
    return {"valid": True, "payload": payload}
