"""draftclaw shared utilities — building codes, design criteria, jurisdiction lookup."""
from pathlib import Path
import re

DRAFTCLAW_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = DRAFTCLAW_DIR.parent.parent
JURISDICTIONS = PROJECT_ROOT / "agents" / "webclaw" / "references" / "lawclaw" / "jurisdictions" / "us"


def lookup_building_codes(city_state: str) -> dict:
    """Search jurisdiction files for building codes, design criteria, permits."""
    parts = city_state.strip().split()
    if len(parts) < 2:
        return {"error": "Provide city and state, e.g. 'Denver CO'"}
    state = parts[-1].upper()
    city = " ".join(parts[:-1])
    result = {"building_codes": [], "design_criteria": [], "permits": [], "urls": [], "municipal_info": []}
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
                # Building codes
                for line in content.split("\n"):
                    if any(kw in line.lower() for kw in ["ibc ", "irc ", "nec ", "ipc ", "imc ", "ifc ", "iecc ", "building code"]):
                        result["building_codes"].append(line.strip()[:200])
                # Design criteria
                for line in content.split("\n"):
                    if any(kw in line.lower() for kw in ["frost depth", "snow load", "wind speed", "seismic", "design criteria"]):
                        result["design_criteria"].append(line.strip()[:200])
                # Permits
                for line in content.split("\n"):
                    if any(kw in line.lower() for kw in ["permit", "building dept", "planning", "community development", "ahj"]):
                        result["permits"].append(line.strip()[:200])
                # URLs
                for line in content.split("\n"):
                    if "https://" in line:
                        url = line[line.index("https://"):].split()[0].rstrip(")")
                        if url not in result["urls"]:
                            result["urls"].append(url)
                # Municipal
                for line in content.split("\n"):
                    if any(kw in line.lower() for kw in ["city and county building", "police department", "library", "hospital"]):
                        result["municipal_info"].append(line.strip()[:200])
            break
    return result
