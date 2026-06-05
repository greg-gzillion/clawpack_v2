"""Browse reference categories"""
from pathlib import Path

WEB_REFS = Path(__file__).resolve().parent.parent / "references"
name = "/browse"

def run(args, agent=None):
    if not args:
        if WEB_REFS.exists():
            cats = sorted([d.name for d in WEB_REFS.iterdir() if d.is_dir()])
            return "Categories: " + ", ".join(cats)
        return "References not found"
    
    cat_path = WEB_REFS / args
    if cat_path.exists():
        files = sorted([f.stem for f in cat_path.rglob("*.md")])
        return f"{args}: " + ", ".join(files[:50])
    return f"Category not found: {args}"
