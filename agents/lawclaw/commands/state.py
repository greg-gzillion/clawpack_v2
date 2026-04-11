"""state command - State courts"""

name = "/state"

def run(args):
    print("\n" + "="*60)
    print("🏛️ STATE COURT SYSTEM")
    print("="*60)
    if args:
        print(f"Looking up: {args.upper()}")
        from core.data import get_state_info
        info = get_state_info(args.upper())
        if info["exists"]:
            print(f"\n{args.upper()} has {info['total']} counties with court data.")
            print(f"Use /browse {args.upper()} to see all counties.")
        else:
            print(f"State '{args}' not found in database.")
    else:
        print("Usage: /state [state code]")
        print("Example: /state TX")
        print("Use /list to see all available states.")
    print("="*60)
