"""docket command - Search dockets"""

name = "/docket"

def run(args):
    print("\n" + "="*60)
    print("📂 DOCKET SEARCH")
    print("="*60)
    if args:
        print(f"Searching docket: {args}")
        print("\nThis will retrieve court docket information.")
    else:
        print("Usage: /docket [case number]")
    print("="*60)
