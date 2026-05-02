"""ClawCoder Schema - Constitutional contract for code generation.

All ClawCoder commands MUST accept this contract.
Schema validation before any code generation or execution.
"""
from typing import Dict, List, Optional
from enum import Enum

class CommandType(str, Enum):
    CODE = "code"
    EXPLAIN = "explain"
    DEBUG = "debug"
    REVIEW = "review"
    TUTORIAL = "tutorial"
    TRANSLATE = "translate"
    RUN = "run"
    TEST = "test"
    SCAN = "scan"
    DOCS = "docs"
    PROJECT = "project"
    DEPS = "deps"
    PERF = "perf"
    DELEGATE = "delegate"

CANONICAL_PAYLOAD = {
    "type": "code",                    # CommandType
    "intent": "generate_code",         # For Truth Resolver
    "task_type": "code_generation",    # For LLM Router
    "confidence": 1.0,                 # For Memory Guard
    "source": "user",                  # "user" | "agent" | "shared"
    "language": "python",             # Target language (auto-detected if empty)
    "query": "async web scraper",      # The task description
    "flags": {
        "validate": True,              # Run compiler validation
        "scan": False,                 # Include project context
        "save": True,                  # Save to exports/
        "export_format": "py",         # File extension override
    },
    "delegate": {
        "target_agent": None,
        "command": None,
        "payload": None,
    }
}

def validate(payload: dict) -> dict:
    """Validate a ClawCoder payload against the constitutional contract."""
    if not isinstance(payload, dict):
        return {"valid": False, "error": "Payload must be a dict"}

    if payload.get("type") == "delegate":
        if "target_agent" not in payload:
            return {"valid": False, "error": "Delegate requires target_agent"}
        payload.setdefault("intent", "agent_delegation")
        payload.setdefault("confidence", 1.0)
        return {"valid": True, "payload": payload}

    cmd_type = payload.get("type", "code")
    if cmd_type not in [e.value for e in CommandType]:
        return {"valid": False, "error": f"Unknown command type: {cmd_type}"}

    payload.setdefault("intent", "generate_code")
    payload.setdefault("task_type", "code_generation")
    payload.setdefault("confidence", 1.0)
    payload.setdefault("source", "user")
    payload.setdefault("language", "")
    payload.setdefault("query", "")
    payload.setdefault("flags", {})
    payload.setdefault("delegate", {})

    return {"valid": True, "payload": payload}
