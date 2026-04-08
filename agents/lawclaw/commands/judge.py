"""judge command - Judge information"""

name = "/judge"

def run(args):
    print("\n" + "="*60)
    print("👨‍⚖️ JUDGE INFORMATION")
    print("="*60)
    if args:
        print(f"Looking up: {args}")
        print("\nThis will show biography, notable rulings, and case history.")
    else:
        print("Usage: /judge [judge name]")
        print("Example: /judge John Roberts")
    print("="*60)
