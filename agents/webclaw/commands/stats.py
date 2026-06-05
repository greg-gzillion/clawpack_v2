"""Reference statistics"""
from pathlib import Path

WEB_REFS = Path(__file__).resolve().parent.parent / "references"
name = "/stats"

def run(args, agent=None):
    if not WEB_REFS.exists():
        return "References not found"
    cats = [d for d in WEB_REFS.iterdir() if d.is_dir()]
    total_files = sum(1 for _ in WEB_REFS.rglob("*.md"))
    lines = [f"Categories: {len(cats)}", f"Total files: {total_files}"]
    for c in sorted(cats):
        count = sum(1 for _ in c.rglob("*.md"))
        lines.append(f"  {c.name}: {count} files")
    return "\n".join(lines)
