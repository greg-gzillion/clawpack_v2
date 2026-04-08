"""browse command - Browse state courts"""

name = "/browse"

def run(args):
    if not args:
        print("Usage: /browse STATE")
        print("Example: /browse TX")
        return
    
    state = args.upper().strip()
    from pathlib import Path
    
    webclaw_path = Path(__file__).parent.parent.parent / "webclaw" / "references" / "lawclaw" / "jurisdictions" / state
    
    if webclaw_path.exists():
        counties = [d.name for d in webclaw_path.iterdir() if d.is_dir()]
        print(f"\n📁 {state} - {len(counties)} counties:\n")
        for i, county in enumerate(counties[:30], 1):
            print(f"  {i:2}. {county}")
        if len(counties) > 30:
            print(f"  ... and {len(counties) - 30} more counties")
        print(f"\n💡 Use /court {state}/COUNTY for details")
    else:
        print(f"❌ No data found for state: {state}")
        print("💡 Use /list to see available states")
