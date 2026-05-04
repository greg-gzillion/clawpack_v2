"""Constitutional Anthropic Contract — enforced structured I/O per Article V & XI"""
from typing import TypedDict, Literal, List, Optional
import json
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
ANTHROPIC_OUTPUT_SCHEMA = {
    "meta": {"agent": "string", "status": "CONCEPTUAL_ONLY"},
    "inputs": {"project": {}, "jurisdiction": {}, "design_criteria": {}, "ahj": {}},
    "derived": {"design_governance": {}},
    "design": {"structural_system": {}, "foundation": {}, "lateral_system": {}},
    "warnings": ["string"]
}

def validate_response(response_text):
    """Validate and clean Anthropic response. Hard reject on violations."""
    text = response_text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        if len(lines) > 1:
            text = "\n".join(lines[1:])
        if text.endswith("```"):
            text = text[:-3]
    text = text.strip()
    
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        raise ValueError("REJECT: Response is not valid JSON")
    
    narrative_flags = ["it appears", "based on the", "please note", "i have followed"]
    text_lower = text.lower()
    for flag in narrative_flags:
        if flag in text_lower:
            raise ValueError("REJECT: Narrative detected")
    
    for section in ["inputs", "design"]:
        for field, value in data.get(section, {}).items():
            if isinstance(value, dict):
                src = value.get("source", "")
                if src and src not in ["chronicle", "web_verified"]:
                    value["source"] = None
                    value["status"] = "INFERRED"
    
    return data