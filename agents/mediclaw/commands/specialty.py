"""specialty command - Find hospitals by medical specialty"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
name = "specialty"

def run(args: str, agent=None) -> str:
    from agents.mediclaw.commands._helpers import lookup_hospitals
    from agents.mediclaw.commands._memory import remember
    
    query = args.strip()
    if not query:
        return "Usage: /specialty <type> in <city ST>\nExamples:\n  /specialty cardiac in Denver CO\n  /specialty pediatric in Miami FL\n  /specialty trauma in Bedford VA"
    
    import re
    match = re.search(r'(.+?)\s+in\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\s*,?\s*[A-Z]{2})', query)
    if not match:
        return "Format: /specialty <type> in <city ST>\nExample: /specialty cardiac in Denver CO"
    
    specialty = match.group(1).strip().lower()
    city_state = match.group(2).strip()
    
    hospitals = lookup_hospitals(city_state)
    if "error" in hospitals:
        return hospitals["error"]
    
    # Filter hospitals by specialty keywords in name
    specialty_keywords = {
        "cardiac": ["heart", "cardiac", "cardiovascular"],
        "pediatric": ["children", "pediatric", "child"],
        "trauma": ["trauma", "emergency", "critical care"],
        "cancer": ["cancer", "oncology", "memorial"],
        "orthopedic": ["orthop", "bone", "joint"],
        "neurology": ["neuro", "brain", "spine"],
        "mental": ["mental", "behavioral", "psychiatric", "counseling"],
        "rehab": ["rehab", "physical therapy", "recovery"],
        "women": ["women", "obstetric", "gynecology", "maternity"],
        "surgical": ["surgery", "surgical", "operating"],
    }
    
    keywords = specialty_keywords.get(specialty, [specialty])
    filtered = []
    for h in hospitals.get("hospitals", []):
        name_lower = h.get("name", "").lower()
        if any(kw in name_lower for kw in keywords):
            filtered.append(h)
    
    if not filtered:
        return f"No {specialty} facilities found in {city_state}. Try a broader search or check /hospital {city_state} for all facilities."
    
    lines = [f"{specialty.title()} Facilities: {hospitals.get('city','')}, {hospitals.get('state','')}", "=" * 60]
    for h in filtered:
        lines.append(f"\n  {h.get('name', 'Unknown')}")
        if h.get('address'): lines.append(f"     {h['address']}")
        if h.get('phone'): lines.append(f"     Phone: {h['phone']}")
    
    result = "\n".join(lines)
    remember(command="specialty", query=query, result_summary=result[:400],
             source_type="web_verified", confidence=0.88)
    return result
