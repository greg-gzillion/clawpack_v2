"""analyze command - Analyze legal text"""

name = "/analyze"

def run(args):
    print("\n" + "="*60)
    print("🔬 LEGAL TEXT ANALYZER")
    print("="*60)
    if args:
        print(f"Analyzing: {args[:100]}...")
        print("\nThis will extract key legal concepts, holdings, and reasoning.")
    else:
        print("Usage: /analyze [legal text to analyze]")
    print("="*60)
