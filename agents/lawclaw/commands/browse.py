"""browse command - Browse state court system"""
from pathlib import Path

name = "/browse"

def run(args):
    if not args:
        return "??? Usage: /browse [state code] (e.g., TX, CA, NY)"
    
    state = args.strip().upper()
    LEGAL_REFS = Path("str(PROJECT_ROOT)/agents/webclaw/references/lawclaw")
    state_path = LEGAL_REFS / "jurisdictions" / state
    
    if not state_path.exists():
        return f"? State '{state}' not found\n?? Use /list to see available states"
    
    output = []
    output.append(f"\n??? EXPLORING {state} COURT SYSTEM")
    output.append("="*50)
    
    counties = [d for d in state_path.iterdir() if d.is_dir()]
    
    if counties:
        output.append(f"\n?? COUNTIES ({len(counties)} total):\n")
        for i, county in enumerate(sorted(counties)[:30], 1):
            court_files = list(county.glob("*.md"))
            output.append(f"  {i:2}. {county.name:<25} - {len(court_files)} courts")
        
        if len(counties) > 30:
            output.append(f"\n  ... and {len(counties) - 30} more counties")
        
        output.append(f"\n?? To view a specific county: /court {state}/COUNTYNAME")
    
    return "\n".join(output)
