def run(args):
    """Analyze code for performance bottlenecks. Usage: /perf python exports/myfile.py"""
    if not args:
        return "Usage: /perf python exports/myfile.py"

    from pathlib import Path

    parts = args.split(maxsplit=1)
    lang = parts[0].lower()
    target = parts[1] if len(parts) > 1 else ""

    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
    EXPORTS = PROJECT_ROOT / "exports"

    if not target:
        return "Usage: /perf python filename.py"

    filepath = EXPORTS / target
    if not filepath.exists():
        return f"File not found: {filepath}\n\nUse /docs {lang} --all to list available files"

    content = filepath.read_text(encoding="utf-8", errors="ignore")

    from agents.claw_coder.agent_handler import _agent
    result = _agent.ask_llm(
        f"Analyze this {lang} code for performance issues. Identify bottlenecks, complexity, and optimization opportunities.\n\nCode:\n{content[:4000]}"
    )
    return f"Performance analysis for {target}:\n\n{result}"