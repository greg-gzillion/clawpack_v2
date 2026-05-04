import json
"""Constitutional Anthropic Contract — enforced structured I/O per Article V & XI"""
from typing import TypedDict, Literal, List, Optional

class DesignCriterion(TypedDict, total=False):
    value: Optional[str]
    source: Optional[Literal["chronicle", "web_verified"]]  # Only these two are constitutionally valid. null = inference.
    status: Literal["VERIFIED", "DESIGN_REQUIRED", "UNKNOWN", "INFERRED"]

class JurisdictionInput(TypedDict):
    name: str
    source: Literal["chronicle"]
    confidence: float
    design_criteria: dict[str, DesignCriterion]
    ahj: dict[str, Optional[str]]

class StructuralInput(TypedDict):
    task: str
    project: str
    jurisdiction: JurisdictionInput
    rules: List[str]

class StructuralOutput(TypedDict, total=False):
    foundation: dict[str, DesignCriterion]
    columns: dict[str, DesignCriterion]
    beams: dict[str, DesignCriterion]
    lateral_system: dict[str, DesignCriterion]
    roof: dict[str, DesignCriterion]
    slab: dict[str, DesignCriterion]
    connections: dict[str, DesignCriterion]
    governing_load: Optional[str]
    delegation_plan: List[str]
    warnings: List[str]

FABRICATION_PATTERNS = [
    r"W\d+x\d+",           # fake steel sizes
    r"\d{3,5}\s*psf",       # soil/capacity assumptions
    r"\d{2,5}\s*kip",       # load assumptions
    r'\d+"\s*x\s*\d+"',     # member dimensions
    r"#\d+\s*(?:rebar|bar)", # rebar specs
]

def validate_output(data: dict) -> StructuralOutput:
    """Validate output before returning to user. Hard fail on violations."""
    for section in ["foundation", "columns", "beams", "lateral_system"]:
        for field, value in data.get(section, {}).items():
            if not isinstance(value, dict):
                raise ValueError(f"Invalid field structure: {section}.{field}")
            if value.get("status") == "VERIFIED" and not value.get("source"):
                raise ValueError(f"VERIFIED field missing source: {section}.{field}")
            if value.get("status") == "VERIFIED" and value.get("value") is None:
                raise ValueError(f"VERIFIED field has null value: {section}.{field}")
    return data