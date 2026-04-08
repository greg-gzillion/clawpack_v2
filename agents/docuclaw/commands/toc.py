"""Generate table of contents"""
name = "/toc"

def run(args):
    if not args:
        print("Usage: /toc <file>")
        return
    from pathlib import Path
    import re
    p = Path(args)
    if not p.exists():
        print(f"File not found: {p}")
        return
    content = p.read_text()
    toc = []
    for line in content.split('\n'):
        m = re.match(r'^(#{1,6})\s+(.+)$', line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            indent = "  " * (level - 1)
            toc.append(f"{indent}- {title}")
    if toc:
        output = p.parent / f"{p.stem}_with_toc.md"
        output.write_text("# Table of Contents\n\n" + "\n".join(toc) + "\n\n---\n\n" + content)
        print(f"✅ TOC added to {output}")
    else:
        print("No headings found")
