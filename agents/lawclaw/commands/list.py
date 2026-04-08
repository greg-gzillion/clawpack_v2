name = "/list"

def run(args):
    from core import get_states
    
    states = get_states()
    print(f"\n{len(states)} states:\n")
    for i, s in enumerate(states, 1):
        print(f"  {s}", end="  ")
        if i % 8 == 0:
            print()
    print()
