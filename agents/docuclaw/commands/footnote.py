"""Add footnote to document"""
name = "/footnote"

def run(args):
    if not args:
        print("Usage: /footnote <file> <reference> <text>")
        return
    from pathlib import Path
    parts = args.split(' ', 2)
    if len(parts) < 3:
        print("Need file, reference, and footnote text")
        return
    p = Path(parts[0])
    if not p.exists():
        print(f"File not found: {p}")
        return
    ref = parts[1]
    text = parts[2]
    content = p.read_text()
    footnote = f"\n\n[{ref}]: {text}\n"
    output = p.parent / f"{p.stem}_with_footnotes.md"
    output.write_text(content + footnote)
    print(f"✅ Footnote added: [{ref}] {text[:50]}...")
