def run(args):
    """Generate documentation for code. Usage: /docs python exports/myfile.py"""
    if not args:
        return "Usage: /docs python exports/myfile.py\n       /docs rust --all"

    from pathlib import Path
    import sys

    parts = args.split(maxsplit=1)
    lang = parts[0].lower()
    target = parts[1] if len(parts) > 1 else ""

    # Use project root from the module path, not hardcoded
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
    EXPORTS = PROJECT_ROOT / "exports"

    if target == "--all":
        ext = {"python": ".py", "rust": ".rs", "go": ".go", "javascript": ".js", "typescript": ".ts"}.get(lang, ".py")
        files = sorted(EXPORTS.glob(f"*{ext}"), key=lambda f: f.stat().st_mtime, reverse=True)[:10]
        if not files:
            return f"No {lang} files found in exports/"
        results = [f"{f.name} ({f.stat().st_size} bytes)" for f in files]
        return f"Found {len(files)} {lang} files:\n" + "\n".join(results)

    if not target:
        return "Usage: /docs python filename.py"

    filepath = EXPORTS / target
    if not filepath.exists():
        return f"File not found: {filepath}\n\nUse /docs {lang} --all to list available files"

    content = filepath.read_text(encoding="utf-8", errors="ignore")

    from agents.claw_coder.agent_handler import _agent
    result = _agent.ask_llm(
        f"Generate documentation for this {lang} code. Add docstrings, usage examples, and API reference.\n\nCode:\n{content[:4000]}"
    )
    return f"Documentation for {target}:\n\n{result}"