"""Add page numbers"""
name = "/pagenum"

def run(args):
    if not args:
        print("Usage: /pagenum <file>")
        return
    from pathlib import Path
    p = Path(args)
    if not p.exists():
        print(f"File not found: {p}")
        return
    content = p.read_text()
    lines = content.split('\n')
    lines_per_page = 50
    total = (len(lines) // lines_per_page) + 1
    output = p.parent / f"{p.stem}_numbered.md"
    output.write_text(content + f"\n\n---\nPage 1 of {total}\n")
    print(f"✅ Page numbers added")
