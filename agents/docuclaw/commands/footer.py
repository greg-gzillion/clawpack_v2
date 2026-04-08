"""Add footer to document"""
name = "/footer"

def run(args):
    if not args:
        print("Usage: /footer <file> <text>")
        return
    from pathlib import Path
    parts = args.split(' ', 1)
    if len(parts) < 2:
        print("Need file and footer text")
        return
    p = Path(parts[0])
    if not p.exists():
        print(f"File not found: {p}")
        return
    footer = parts[1]
    content = p.read_text()
    output = p.parent / f"{p.stem}_with_footer.md"
    output.write_text(content + f"\n\n---\n{footer}\n")
    print(f"✅ Footer added: {footer}")
