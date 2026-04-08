"""summarize command - Summarize cases"""

name = "/summarize"

def run(args):
    print("\n" + "="*60)
    print("📝 CASE SUMMARIZER")
    print("="*60)
    if args:
        print(f"Summarizing: {args}")
        print("\nThis will generate a case brief with facts, issue, holding, reasoning.")
    else:
        print("Usage: /summarize [case name or text]")
    print("="*60)
