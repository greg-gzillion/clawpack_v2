from core.data import get_data_path
from utils.helpers import truncate

def court_command(location):
    if not location:
        print("Usage: /court TX or /court TX/DALLAS")
        return
    
    location = location.strip().upper()
    data_path = get_data_path()
    
    if '/' in location:
        state, county = location.split('/', 1)
        _show_county(data_path, state, county)
    else:
        _show_state(data_path, location)

def _show_state(data_path, state):
    state_path = data_path / "jurisdictions" / state
    if not state_path.exists():
        print(f"No data found for {state}")
        return
    
    counties = [d for d in state_path.iterdir() if d.is_dir()]
    print(f"\n{state} COURT SYSTEM")
    print("="*50)
    print(f"Counties: {len(counties)}")
    print(f"\nUse /browse {state} to list all counties")

def _show_county(data_path, state, county):
    county_path = data_path / "jurisdictions" / state / county
    if not county_path.exists():
        state_path = data_path / "jurisdictions" / state
        if state_path.exists():
            for d in state_path.iterdir():
                if d.is_dir() and d.name.upper() == county:
                    county_path = d
                    break
    
    if not county_path or not county_path.exists():
        print(f"No data found for {county} County, {state}")
        return
    
    print(f"\n{county_path.name.upper()} COUNTY, {state}")
    print("="*50)
    
    for cf in sorted(county_path.glob("*.md")):
        content = cf.read_text(encoding='utf-8', errors='ignore')
        lines = content.split('\n')
        title = lines[0].replace('#', '').strip() if lines else cf.stem
        print(f"\n{title}")
        print("-"*40)
        print(truncate(content))
