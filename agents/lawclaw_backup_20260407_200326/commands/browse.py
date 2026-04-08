from core.data import get_data_path

def browse_command(state):
    if not state:
        print("Usage: /browse TX")
        return
    
    state = state.strip().upper()
    data_path = get_data_path()
    state_path = data_path / "jurisdictions" / state
    
    if not state_path.exists():
        print(f"State '{state}' not found")
        return
    
    counties = [d for d in state_path.iterdir() if d.is_dir()]
    print(f"\n{state} - {len(counties)} COUNTIES")
    print("="*50)
    for county in sorted(counties)[:30]:
        court_files = list(county.glob("*.md"))
        print(f"  {county.name}: {len(court_files)} courts")
    if len(counties) > 30:
        print(f"\n  ... and {len(counties)-30} more")
    print(f"\nTo view a county: /court {state}/COUNTYNAME")
