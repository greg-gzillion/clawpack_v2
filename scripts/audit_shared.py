from pathlib import Path
import re

shared = Path("shared")
categories = {"llm": [], "memory": [], "enforcement": [], "hooks": [], "files": [], "search": [], "skills": [], "core": []}

for f in sorted(shared.rglob("*.py")):
    if "__pycache__" in str(f): continue
    rel = str(f.relative_to(shared))
    content = f.read_text(encoding="utf-8", errors="ignore")
    lines = len(content.split("\n"))
    has_class = bool(re.search(r"class\s+(\w+)", content))

    imported_by = []
    for agent_dir in Path("agents").iterdir():
        if not agent_dir.is_dir() or agent_dir.name.startswith("_"): continue
        for py_file in agent_dir.rglob("*.py"):
            if "__pycache__" in str(py_file): continue
            try:
                ac = py_file.read_text(encoding="utf-8", errors="ignore")
                if f"from shared.{f.stem} import" in ac or f"import shared.{f.stem}" in ac:
                    if agent_dir.name not in imported_by:
                        imported_by.append(agent_dir.name)
            except: pass

    if "llm" in rel: cat = "llm"
    elif "memory" in rel: cat = "memory"
    elif "enforcement" in rel: cat = "enforcement"
    elif "hooks" in rel: cat = "hooks"
    elif "files" in rel: cat = "files"
    elif "search" in rel: cat = "search"
    elif "skills" in rel: cat = "skills"
    else: cat = "core"

    status = "USED" if imported_by else "UNUSED"
    categories[cat].append((rel, lines, has_class, status, imported_by[:3]))

for cat, files in categories.items():
    if not files: continue
    print(f"\n=== {cat.upper()} ({len(files)} files) ===")
    for rel, lines, has_class, status, importers in sorted(files):
        flag = "YES" if status == "USED" else "NO "
        cls = "class" if has_class else "func"
        importers_str = ", ".join(importers) if importers else "none"
        print(f"  {flag} {rel:<40} {lines:>4}L {cls:<5} imported_by={importers_str}")
