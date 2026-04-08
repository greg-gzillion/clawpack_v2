name = "/stats"

def run(args):
    from core import LAW_REFS, get_states, get_api_key
    
    print("\n" + "="*50)
    print("SYSTEM STATISTICS")
    print("="*50)
    print(f"API: {'✅' if get_api_key() else '❌'}")
    if LAW_REFS.exists():
        print(f"Reference Files: {len(list(LAW_REFS.rglob('*.md')))}")
    print(f"States: {len(get_states())}")
    print("="*50)
