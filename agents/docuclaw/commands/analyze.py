"""Analyze document command"""
name = "/analyze"
def run(args):
    if not args:
        print("Usage: /analyze <filename>")
        return
    from pathlib import Path
    p = Path(args)
    if not p.exists():
        print(f"File not found: {args}")
        return
    content = p.read_text()
    lines = len(content.split('\n'))
    words = len(content.split())
    chars = len(content)
    print(f"\n📊 Analysis of {p.name}:")
    print(f"  Lines: {lines}")
    print(f"  Words: {words}")
    print(f"  Characters: {chars}")
