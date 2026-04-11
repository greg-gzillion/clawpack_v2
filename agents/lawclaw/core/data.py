"""Data access - search, states, counties"""

from .config import LAW_REFS
import re

def search_local(query, max_results=10):
    results = []
    if not LAW_REFS.exists():
        return results
    
    for md in LAW_REFS.rglob("*.md"):
        try:
            content = md.read_text(encoding='utf-8', errors='ignore')
            if query.lower() in content.lower():
                urls = re.findall(r'https?://[^\s\)\]>]+', content)
                results.append({
                    "file": md.name,
                    "content": content[:500],
                    "urls": urls[:3]
                })
                if len(results) >= max_results:
                    break
        except:
            pass
    return results

def get_states():
    juris = LAW_REFS / "jurisdictions"
    if juris.exists():
        return sorted([d.name for d in juris.iterdir() if d.is_dir()])
    return []

def get_state_info(state):
    state_path = LAW_REFS / "jurisdictions" / state.upper()
    if state_path.exists():
        counties = [d.name for d in state_path.iterdir() if d.is_dir()]
        return {"exists": True, "counties": counties[:30], "total": len(counties)}
    return {"exists": False}

def get_county_info(state, county):
    state_path = LAW_REFS / "jurisdictions" / state.upper()
    if not state_path.exists():
        return None
    
    county_path = None
    for d in state_path.iterdir():
        if d.is_dir() and d.name.upper() .lower() == county.lower().upper():
            county_path = d
            break
    
    if not county_path:
        return None
    
    courts = []
    for cf in county_path.glob("*.md"):
        content = cf.read_text(encoding='utf-8', errors='ignore')
        title = content.split('\n')[0].replace('#', '').strip()
        courts.append({"name": title, "content": content[:500]})
    
    return {"county": county_path.name, "courts": courts}
