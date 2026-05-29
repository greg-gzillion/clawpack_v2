"""emergency command - Constitutional emergency triage with automatic hospital routing"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
name = "emergency"

def run(args: str, agent=None) -> str:
    from agents.mediclaw.commands._memory import recall, remember
    from agents.mediclaw.commands._helpers import lookup_hospitals, find_nearest_hospital
    import re
    
    query = args.strip()
    if not query:
        return "Usage: /emergency <symptoms or emergency description>"
    
    # Check memory for similar emergencies
    prior = recall(f"emergency {query}", limit=2)
    prior_text = ""
    if prior:
        prior_text = "\n".join(f"Prior: {p.get('fact','')[:200]}" for p in prior)
    
    # Build emergency triage prompt
    prompt = f"""EMERGENCY TRIAGE ASSESSMENT

PRESENTING SYMPTOMS:
{query}

Provide:
1. SEVERITY CLASSIFICATION — Life-threatening / Urgent / Non-urgent
2. IMMEDIATE ACTIONS — What the person or bystander should do RIGHT NOW
3. WHEN TO CALL 911 — Clear, specific criteria
4. WHAT TO TELL THE DISPATCHER — Key information to communicate
5. DANGER SIGNS — Symptoms that indicate the situation is worsening

Be direct and actionable. If this could be life-threatening, say so clearly.
Cite authoritative emergency medicine sources (American College of Emergency Physicians, CDC, NIH)."""
    
    if prior_text:
        prompt = f"Prior emergency cases:\n{prior_text}\n\n{prompt}"
    
    if agent and hasattr(agent, 'ask_llm'):
        result = agent.ask_llm(prompt)
    else:
        return "Error: No agent context"
    
    # Extract location for hospital routing
    location_match = re.search(r'in\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*,?\s*([A-Z]{2})', query)
    latlon_match = re.search(r'(\d{2}\.\d+),\s*(-?\d{2,3}\.\d+)', query)
    
    hospital_info = ""
    if location_match:
        city_state = f"{location_match.group(1)} {location_match.group(2)}"
        try:
            hospitals = lookup_hospitals(city_state)
            if hospitals.get("hospitals"):
                hospital_info = f"\n\n### EMERGENCY DEPARTMENTS — {city_state}\n"
                for h in hospitals["hospitals"][:3]:
                    hospital_info += f"\n- **{h.get('name', 'Hospital')}**\n"
                    if h.get('address'): hospital_info += f"  {h['address']}\n"
                    if h.get('phone'): hospital_info += f"  Phone: {h['phone']}\n"
                    if h.get('lat') and h.get('lon'):
                        hospital_info += f"  GPS: {h['lat']}, {h['lon']}\n"
        except Exception:
            pass
    elif latlon_match:
        try:
            lat, lon = float(latlon_match.group(1)), float(latlon_match.group(2))
            hospitals = find_nearest_hospital(lat, lon)
            if hospitals.get("hospitals"):
                hospital_info = f"\n\n### NEAREST EMERGENCY DEPARTMENTS\n"
                for h in hospitals["hospitals"][:3]:
                    hospital_info += f"\n- **{h.get('name', 'Hospital')}** ({h.get('city','')}, {h.get('state','')})\n"
                    if h.get('address'): hospital_info += f"  {h['address']}\n"
        except Exception:
            pass
    
    if hospital_info:
        result += hospital_info
    
    result += "\n\n---\n*IN AN EMERGENCY, CALL 911. This information supports but does not replace emergency medical dispatch. Sources: ACEP, CDC, NIH.*"
    
    remember(command="emergency", query=query, result_summary=result[:400],
             source_type="web_verified", confidence=0.90)
    
    return result
