"""Add header to document"""
name = "/header"

def run(args):
    if not args:
        print("Usage: /header <file> <text>")
        return
    from pathlib import Path
    parts = args.split(' ', 1)
    if len(parts) < 2:
        print("Need file and header text")
        return
    p = Path(parts[0])
    if not p.exists():
        print(f"File not found: {p}")
        return
    header = parts[1]
    content = p.read_text()
    output = p.parent / f"{p.stem}_with_header.md"
    output.write_text(f"---\nheader: {header}\n---\n\n{content}")
    print(f"✅ Header added: {header}")
