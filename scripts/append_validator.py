path = r"C:\Users\greg\dev\clawpack_v2\shared\anthropic_contract.py"
with open(path, encoding="utf-8") as f:
    content = f.read()

# Add json import at top if missing
if "import json" not in content:
    content = "import json\n" + content

# Append the output schema and validate_response
append = r"""

ANTHROPIC_OUTPUT_SCHEMA = {
    "meta": {"agent": "string", "status": "CONCEPTUAL_ONLY"},
    "inputs": {"project": {}, "jurisdiction": {}, "design_criteria": {}, "ahj": {}},
    "derived": {"design_governance": {}},
    "design": {"structural_system": {}, "foundation": {}, "lateral_system": {}},
    "warnings": ["string"]
}

def validate_response(response_text: str) -> dict:
    """Validate and clean Anthropic response. Hard reject on violations."""
    text = response_text.strip()
    # Strip markdown code blocks
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
    
    # Reject narrative
    narrative_flags = ["it appears", "based on the", "please note", "i have followed"]
    text_lower = text.lower()
    for flag in narrative_flags:
        if flag in text_lower:
            raise ValueError("REJECT: Narrative detected")
    
    # Reject fabricated sources
    for section in ["inputs", "design"]:
        for field, value in data.get(section, {}).items():
            if isinstance(value, dict):
                src = value.get("source", "")
                if src and src not in ["chronicle", "web_verified"]:
                    value["source"] = None
                    value["status"] = "INFERRED"
    
    return data
"""

content = content + append

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Added validate_response and output schema")
