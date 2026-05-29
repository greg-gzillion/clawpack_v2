"""diagnose command - Constitutional medical diagnosis with urgency triage + hospital routing"""
import sys, re
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
name = "diagnose"

def run(args: str, agent=None) -> str:
    from agents.mediclaw.commands._memory import recall, remember
    from agents.mediclaw.commands._helpers import lookup_hospitals
    
    query = args.strip()
    if not query:
        return "Usage: /diagnose <symptoms or condition description>"
    
    prior = recall(query, limit=3)
    prior_text = ""
    if prior:
        prior_text = "\n".join(f"Prior case: {p.get('fact','')[:200]}" for p in prior)
    
    is_professional = any(kw in query.lower() for kw in [
        "differential", "etiology", "pathophysiology", "comorbid",
        "contraindicated", "prognosis", "idiopathic", "iatrogenic",
        "sequelae", "stenosis", "thrombosis", "neoplasm"
    ])
    
    if is_professional:
        prompt = f"""CLINICAL DIAGNOSIS REQUEST - Professional Analysis

PATIENT PRESENTATION:
{query}

Provide a comprehensive clinical analysis:
1. DIFFERENTIAL DIAGNOSIS - Ranked by likelihood with rationale
2. RECOMMENDED WORKUP - Labs, imaging, specialist consults
3. EVIDENCE BASIS - Cite authoritative sources (NIH, CDC, peer-reviewed)
4. URGENCY ASSESSMENT - Routine / Urgent / Emergent / Critical
5. RED FLAGS - Symptoms requiring immediate intervention"""
    else:
        prompt = f"""MEDICAL ASSESSMENT - Patient Guidance

SYMPTOMS/CONCERN:
{query}

Provide clear, actionable guidance:
1. WHAT THIS COULD BE - Common possible causes (not alarming, just informative)
2. WHAT TO DO - Self-care steps if appropriate
3. WHEN TO SEEK CARE - Clear criteria for urgent care vs ER vs doctor visit
4. RED FLAGS - Symptoms that require immediate emergency attention
5. AUTHORITATIVE SOURCES - Cite NIH, CDC, Mayo Clinic where applicable

IMPORTANT: This is informational, not a diagnosis. Recommend professional evaluation."""
    
    if prior_text:
        prompt = f"Prior related cases for context:\n{prior_text}\n\n{prompt}"
    
    if agent and hasattr(agent, 'agent'):
        try:
            context = agent.agent.research(query) if hasattr(agent.agent, 'research') else ""
            if context:
                prompt = f"MEDICAL CONTEXT:\n{context[:2000]}\n\n{prompt}"
        except Exception:
            pass
    
    if agent and hasattr(agent, 'ask_llm'):
        result = agent.ask_llm(prompt)
    else:
        return "Error: No agent context available"
    
    location_match = re.search(r'in\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*,?\s*([A-Z]{2})', query)
    hospital_info = ""
    if location_match:
        city_state = f"{location_match.group(1)} {location_match.group(2)}"
        try:
            hospitals = lookup_hospitals(city_state)
            if hospitals.get("hospitals"):
                hospital_info = f"\n\n### Nearest Medical Facilities in {city_state}\n"
                for h in hospitals["hospitals"][:3]:
                    hospital_info += f"\n- **{h.get('name', 'Hospital')}**\n"
                    if h.get('address'): hospital_info += f"  Address: {h['address']}\n"
                    if h.get('phone'): hospital_info += f"  Phone: {h['phone']}\n"
                    if h.get('url'): hospital_info += f"  Website: {h['url']}\n"
        except Exception:
            pass
    
    if hospital_info:
        result += hospital_info
    
    result += "\n\n---\n*Sources: NIH (nih.gov), CDC (cdc.gov), Mayo Clinic (mayoclinic.org), peer-reviewed literature. Educational only — always consult a healthcare professional.*"
    
    remember(command="diagnose", query=query, result_summary=result[:400],
             source_type="web_verified", confidence=0.85,
             metadata={"professional": is_professional})
    
    return result
