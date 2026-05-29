"""designclaw shared utilities — brand tools + building code lookup."""
from pathlib import Path
from datetime import datetime

DESIGNCLAW_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = DESIGNCLAW_DIR.parent.parent
EXPORTS = PROJECT_ROOT / "exports"
JURISDICTIONS = PROJECT_ROOT / "agents" / "webclaw" / "references" / "lawclaw" / "jurisdictions" / "us"

def lookup_building_codes(city_state: str) -> dict:
    parts = city_state.strip().split()
    if len(parts) < 2:
        return {"error": "Provide city and state, e.g. 'Denver CO'"}
    state = parts[-1].upper()
    city = " ".join(parts[:-1])
    result = {"building_codes": [], "permits": [], "municipal_info": [], "urls": []}
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
                if "Building Code" in content or "building_code" in md_file.name:
                    for line in content.split("\n"):
                        if any(kw in line.lower() for kw in ["ibc ", "irc ", "nec ", "ipc ", "imc ", "ifc ", "iecc ", "building code", "frost depth", "snow load", "wind speed", "seismic"]):
                            result["building_codes"].append(line.strip()[:200])
                if "permit" in content.lower() or "building dept" in content.lower():
                    for line in content.split("\n"):
                        if any(kw in line.lower() for kw in ["permit", "building dept", "planning", "community development"]):
                            result["permits"].append(line.strip()[:200])
                for line in content.split("\n"):
                    if "https://" in line:
                        url = line[line.index("https://"):].split()[0].rstrip(")")
                        if url not in result["urls"]:
                            result["urls"].append(url)
                if "municipal_court" in md_file.name or "law_resources" in md_file.name:
                    for line in content.split("\n"):
                        if any(kw in line.lower() for kw in ["city and county building", "police department", "library", "hospital"]):
                            result["municipal_info"].append(line.strip()[:200])
            break
    if not result["building_codes"] and not result["urls"]:
        return {"error": f"No building code data found for {city}, {state}"}
    return result

def save_html(content: str, name: str) -> str:
    import os
    EXPORTS.mkdir(exist_ok=True)
    html = content
    if "```html" in html:
        html = html.split("```html")[1].split("```")[0]
    elif "```" in html:
        blocks = html.split("```")
        for i, block in enumerate(blocks):
            if i % 2 == 1:
                html = block; break
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fn = f"{name}_{ts}.html"
    filepath = EXPORTS / fn
    filepath.write_text(html, encoding="utf-8")
    try:
        os.startfile(str(filepath))
    except Exception: pass
    return fn
