"""Set page layout"""
name = "/layout"

def run(args):
    if not args:
        print("Usage: /layout <file> [a4|letter] [portrait|landscape]")
        return
    from pathlib import Path
    parts = args.split()
    p = Path(parts[0])
    if not p.exists():
        print(f"File not found: {p}")
        return
    size = parts[1] if len(parts) > 1 else "letter"
    orientation = parts[2] if len(parts) > 2 else "portrait"
    content = p.read_text()
    layout = f"<!-- layout: size={size}, orientation={orientation} -->\n\n"
    output = p.parent / f"{p.stem}_layouted.md"
    output.write_text(layout + content)
    print(f"✅ Layout set: {size}, {orientation}")
    print(f"   Saved to: {output}")
