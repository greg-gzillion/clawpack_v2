name = "/ask"

def run(args):
    if not args:
        print("Usage: /ask [question]")
        return
    from core import ask_ai
    print(f"\nQ: {args}\n")
    print(ask_ai(args))
