"""jurisdiction command - Jurisdiction info"""

name = "/jurisdiction"

def run(args):
    print("\n" + "="*60)
    print("📍 JURISDICTION INFORMATION")
    print("="*60)
    print("""
Types of Jurisdiction:
  • Subject Matter Jurisdiction - Court's authority over case type
  • Personal Jurisdiction - Court's authority over parties
  • Original Jurisdiction - Trial court authority
  • Appellate Jurisdiction - Appeal court authority
  • Federal Question - Cases under Constitution/US laws
  • Diversity Jurisdiction - Parties from different states

Use /federal for federal courts, /state for state courts.
""")
