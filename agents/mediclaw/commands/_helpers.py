"""mediclaw shared utilities — hospital lookup via cache + WebClaw pipeline."""
from pathlib import Path
import re

MEDICLAW_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = MEDICLAW_DIR.parent.parent


def lookup_hospitals(city_state: str, agent=None) -> dict:
    """Query hospitals via agent.cached_search() — cache first, WebClaw fallback.
    All jurisdiction data is indexed in Chronicle FTS5.
    Returns structured dict with name, address, phone, url, coordinates."""
    parts = city_state.strip().split()
    if len(parts) < 2:
        return {"error": "Provide city and state, e.g. Denver CO"}

    state = parts[-1].upper()
    city = " ".join(parts[:-1])

    if not agent or not hasattr(agent, "cached_search"):
        return {"error": "Agent not available for cached search"}

    # Use the existing cache pipeline: DataClaw cache -> WebClaw fallback -> cache write
    result = agent.cached_search(f"hospital {city} {state}")
    if not result:
        return {"city": city, "state": state, "hospitals": [], "count": 0}

    # Parse hospital entries from cached/retrieved results
    # WebClaw returns structured format with content blocks after --- markers
    # Find ## Hospitals sections within those blocks
    hospitals = []
    seen = set()
    
    # Split on --- to get content blocks, then find ## Hospitals
    blocks = str(result).split("---")
    for block in blocks:
        # Find the ## Hospitals section
        hosp_match = re.search(r'## Hospitals\s*\n(.*?)(?:\n## |\Z)', block, re.S)
        if not hosp_match:
            continue
        
        hosp_content = hosp_match.group(1)
        
        lines_list = hosp_content.split("\n")
        for i, line in enumerate(lines_list):
            line = line.strip()
            if not line.startswith("-"):
                continue
            line = line.lstrip("-").strip()
            
            # Must have address or phone indicators
            if not re.search(r"\d{3}[-.]\d{4}|\d+\s+[A-Z]", line):
                continue
            
            parts_line = [p.strip() for p in re.split(r"\s*[—–-]\s*", line)]
            if len(parts_line) < 2:
                continue
            
            name = parts_line[0][:100]
            if name in seen:
                continue
            seen.add(name)
            
            h = {"name": name, "city": city, "state": state}
            
            for p in parts_line[1:]:
                if re.search(r"\d+\s+[A-Z]", p):
                    h["address"] = p
                    break
            
            pm = re.search(r"\(?\d{3}\)?\s*\d{3}[-.]\d{4}", line)
            if pm:
                h["phone"] = pm.group(0)
            
            um = re.search(r"(https?://[^\s\)]+)", line)
            if um:
                h["url"] = um.group(1).rstrip(")")
            
            # Capture URL from next line (Website: format)
            if not h.get("url") and i + 1 < len(lines_list):
                next_line = lines_list[i + 1].strip()
                url_match = re.search(r"(https?://[^\s\)]+)", next_line)
                if url_match:
                    h["url"] = url_match.group(1).rstrip(")")
            
            cm = re.search(r"(\d{2}\.\d+).*?[NS].*?(\d{2,3}\.\d+).*?[EW]", line)
            if cm:
                h["lat"] = float(cm.group(1))
                h["lon"] = float(cm.group(2))
            
            hospitals.append(h)

    return {"city": city, "state": state, "hospitals": hospitals, "count": len(hospitals)}


def find_nearest_hospital(lat: float, lon: float, agent=None, max_distance_km: float = 50) -> dict:
    """Find nearest hospital via Chronicle FTS5 coordinate search."""
    import math
    try:
        from agents.webclaw.core.chronicle_ledger import get_chronicle
        chronicle = get_chronicle()
        results = chronicle.recover_by_context("hospital", limit=100)
        nearest = None
        nearest_dist = float("inf")
        for r in results:
            ctx = r.get("context", "") if isinstance(r, dict) else str(r)
            coord_matches = re.findall(r"(\d{2}\.\d+).*?[NS].*?(\d{2,3}\.\d+).*?[EW]", ctx)
            for clat, clon in coord_matches:
                dlat, dlon = float(clat), float(clon)
                dist = math.sqrt((dlat - lat)**2 + (dlon - lon)**2) * 111
                if dist < nearest_dist and dist < max_distance_km:
                    nearest_dist = dist
                    nearest = {"lat": dlat, "lon": dlon, "distance_km": round(dist, 1)}
        if nearest and agent:
            for r in results:
                ctx = r.get("context", "") if isinstance(r, dict) else str(r)
                if f"{nearest['lat']}" in ctx:
                    city_match = re.search(r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*[—–-]", ctx)
                    if city_match:
                        return lookup_hospitals(f"{city_match.group(1)} CO", agent=agent)
                    break
            return {"error": "Hospital found but location unknown"}
        return {"error": "No hospitals found within range"}
    except Exception as e:
        return {"error": f"Search failed: {e}"}
