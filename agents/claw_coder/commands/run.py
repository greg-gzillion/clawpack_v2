def run(args):
    """Execute code and return output."""
    if not args:
        return "Usage: /run python filename.py"

    import subprocess
    from pathlib import Path

    parts = args.split(maxsplit=1)
    lang = parts[0].lower()
    target = parts[1] if len(parts) > 1 else ""

    # Use absolute path to project root
    PROJECT_ROOT = Path("C:/Users/greg/dev/clawpack_v2")
    EXPORTS = PROJECT_ROOT / "exports"

    if not target:
        # List recent files for this language
        ext = {"python": ".py", "rust": ".rs", "go": ".go", "javascript": ".js", "typescript": ".ts"}.get(lang, "")
        files = sorted(EXPORTS.glob(f"*{ext}"), key=lambda f: f.stat().st_mtime, reverse=True)[:10]
        file_list = "\n".join(f"  {f.name}" for f in files)
        return f"Usage: /run {lang} filename.py\n\nRecent {lang} files:\n{file_list}"

    filepath = EXPORTS / target

    commands = {
        "python": ["python", str(filepath)],
        "go": ["go", "run", str(filepath)],
        "javascript": ["node", str(filepath)],
    }

    cmd = commands.get(lang)
    if not cmd:
        return f"Supported: python, go, javascript"

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=str(PROJECT_ROOT))
        output = result.stdout.strip() or result.stderr.strip()
        status = "OK" if result.returncode == 0 else f"Exit {result.returncode}"
        return f"[{status}]\n{output}"
    except FileNotFoundError:
        return f"{lang} runtime not installed"
    except Exception as e:
        return f"Error: {e}"