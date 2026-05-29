"""mediclaw shared utilities — medical tools + hospital lookup from jurisdiction data."""
from pathlib import Path
import re

MEDICLAW_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = MEDICLAW_DIR.parent.parent
JURISDICTIONS = PROJECT_ROOT / "agents" / "webclaw" / "references" / "lawclaw" / "jurisdictions" / "us"


def lookup_hospitals(city_state: str) -> dict:
    """Search jurisdiction files for hospital data including coordinates.
    Returns: dict with hospitals list, each containing name, address, phone, url, coordinates
    """
    parts = city_state.strip().split()
    if len(parts) < 2:
        return {"error": "Provide city and state, e.g. 'Denver CO'"}
    
    state = parts[-1].upper()
    city = " ".join(parts[:-1])
    
    hospitals = []
    search_path = JURISDICTIONS / state
    
    if not search_path.exists():
        return {"error": f"No jurisdiction data for {state}"}
    
    for city_dir in search_path.iterdir():
        if not city_dir.is_dir(): continue
        if city.lower() in city_dir.name.lower():
            for md_file in city_dir.rglob("*.md"):
                try:
                    content = md_file.read_text(encoding="utf-8", errors="ignore")
                except Exception: continue
                
                # Extract hospital entries
                if "hospital" in content.lower():
                    # Find hospital sections
                    sections = re.split(r'\n(?:###|##)\s+', content)
                    for section in sections:
                        if 'hospital' in section.lower():
                            hospital = {"city": city, "state": state}
                            
                            # Extract name
                            name_match = re.search(r'(?:Hospital|Medical Center|Medical Center)\s*[-–—]\s*(.+?)(?:\n|$)', section)
                            if name_match:
                                hospital["name"] = name_match.group(1).strip()[:100]
                            elif 'hospital' in section.lower():
                                for line in section.split('\n'):
                                    if 'hospital' in line.lower() and '—' in line:
                                        hospital["name"] = line.split('—')[-1].strip()[:100]
                                        break
                            
                            # Extract address
                            addr_match = re.search(r'(\d+\s+[A-Z].+?)\s*[-–—]\s*\(', section)
                            if addr_match:
                                hospital["address"] = addr_match.group(1).strip()
                            
                            # Extract phone
                            phone_match = re.search(r'\(?\d{3}\)?\s*\d{3}[-.]\d{4}', section)
                            if phone_match:
                                hospital["phone"] = phone_match.group(0)
                            
                            # Extract URL
                            url_match = re.search(r'(https?://[^\s\)]+)', section)
                            if url_match:
                                hospital["url"] = url_match.group(1).rstrip(')')
                            
                            # Extract coordinates (lat, lon)
                            coord_match = re.search(r'(\d{2}\.\d{4,})°\s*[NS],?\s*(\d{2,3}\.\d{4,})°\s*[EW]', section)
                            if coord_match:
                                hospital["lat"] = float(coord_match.group(1))
                                hospital["lon"] = float(coord_match.group(2))
                            
                            if hospital.get("name"):
                                hospitals.append(hospital)
            
            break  # Found the city
    
    return {"city": city, "state": state, "hospitals": hospitals, "count": len(hospitals)}


def find_nearest_hospital(lat: float, lon: float, max_distance_km: float = 50) -> dict:
    """Search all jurisdiction files to find the nearest hospital to given coordinates."""
    import math
    
    nearest = None
    nearest_dist = float('inf')
    
    for state_dir in JURISDICTIONS.iterdir():
        if not state_dir.is_dir(): continue
        for city_dir in state_dir.iterdir():
            if not city_dir.is_dir(): continue
            for md_file in city_dir.rglob("*.md"):
                try:
                    content = md_file.read_text(encoding="utf-8", errors="ignore")
                except Exception: continue
                
                coord_matches = re.findall(r'(\d{2}\.\d{4,})°\s*[NS],?\s*(\d{2,3}\.\d{4,})°\s*[EW]', content)
                for clat, clon in coord_matches:
                    dlat = float(clat)
                    dlon = float(clon)
                    # Simple distance (not great-circle, but sufficient for <50km)
                    dist = math.sqrt((dlat - lat)**2 + (dlon - lon)**2) * 111  # rough km
                    if dist < nearest_dist and dist < max_distance_km:
                        nearest_dist = dist
                        nearest = {
                            "city": city_dir.name, "state": state_dir.name,
                            "lat": dlat, "lon": dlon, "distance_km": round(dist, 1)
                        }
    
    if nearest:
        return lookup_hospitals(f"{nearest['city']} {nearest['state']}")
    return {"error": "No hospitals found within range"}
