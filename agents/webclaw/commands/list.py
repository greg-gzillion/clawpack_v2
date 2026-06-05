"""List reference files"""
from pathlib import Path

WEB_REFS = Path(__file__).resolve().parent.parent / "references"
name = "/list"

def run(args, agent=None):
    if not WEB_REFS.exists():
        return "References not found"
    cats = sorted([d.name for d in WEB_REFS.iterdir() if d.is_dir()])
    return "Categories: " + ", ".join(cats)
