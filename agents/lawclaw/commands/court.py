"""court command - Get court information"""

name = "/court"

def run(args):
    if not args or "/" not in args:
        print("Usage: /court STATE/COUNTY")
        print("Example: /court CO/CLEAR CREEK")
        return
    
    state, county = args.split("/", 1)
    state = state.upper().strip()
    county = county.upper().strip()
    
    print(f"\n🔍 Looking up court data for {county} County, {state}...")
    
    # Try to read from webclaw references
    import os
    from pathlib import Path
    
    webclaw_path = Path(__file__).parent.parent.parent / "webclaw" / "references" / "lawclaw" / "jurisdictions" / state / county
    
    if webclaw_path.exists():
        print(f"\n📁 Found data for {county} County, {state}:")
        for md_file in webclaw_path.glob("*.md"):
            print(f"  📄 {md_file.stem.replace('_', ' ').title()}")
            
            # Show first few lines of content
            content = md_file.read_text(encoding='utf-8', errors='ignore')
            lines = content.split("\n")[:5]
            for line in lines:
                if line.strip() and not line.startswith("#"):
                    print(f"     {line[:80]}...")
                    break
            print()
    else:
        print(f"❌ No court data found for {county} County, {state}")
        print("💡 Use /list to see available states")
