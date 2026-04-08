"""oral command - Oral arguments"""

name = "/oral"

def run(args):
    print("\n" + "="*60)
    print("🎙️ ORAL ARGUMENTS")
    print("="*60)
    if args:
        print(f"Finding oral arguments for: {args}")
        print("\nThis will locate audio/transcripts of oral arguments.")
    else:
        print("Usage: /oral [case name]")
        print("Example: /oral Roe v. Wade")
    print("="*60)
