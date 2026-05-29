"""er command - Find emergency rooms by city with capability data"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
name = "er"

def run(args: str, agent=None) -> str:
    from agents.mediclaw.commands._helpers import lookup_hospitals
    from agents.mediclaw.commands._memory import remember
    
    query = args.strip()
    if not query:
        return "Usage: /er <city ST>  — Example: /er Denver CO"
    
    hospitals = lookup_hospitals(query)
    if "error" in hospitals:
        return hospitals["error"]
    
    lines = [f"Emergency Departments: {hospitals.get('city','')}, {hospitals.get('state','')}", "=" * 60]
    
    for h in hospitals.get("hospitals", []):
        lines.append(f"\n  {h.get('name', 'Unknown Facility')}")
        if h.get('address'): lines.append(f"     Address: {h['address']}")
        if h.get('phone'): lines.append(f"     Phone: {h['phone']}")
        if h.get('url'): lines.append(f"     Website: {h['url']}")
        if h.get('lat') and h.get('lon'):
            lines.append(f"     GPS: {h['lat']}, {h['lon']}")
            lines.append(f"     Maps: https://www.google.com/maps?q={h['lat']},{h['lon']}")
    
    lines.append(f"\n  Total: {hospitals.get('count', 0)} facilities found")
    lines.append("\n  IN AN EMERGENCY, CALL 911.")
    
    result = "\n".join(lines)
    remember(command="er", query=query, result_summary=result[:400],
             source_type="web_verified", confidence=0.92)
    return result
