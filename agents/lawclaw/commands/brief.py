"""brief command - Find briefs"""

name = "/brief"

def run(args):
    print("\n" + "="*60)
    print("📄 LEGAL BRIEFS")
    print("="*60)
    if args:
        print(f"Finding briefs for: {args}")
        print("\nThis will locate petitioner, respondent, and amicus briefs.")
    else:
        print("Usage: /brief [case name]")
    print("="*60)
