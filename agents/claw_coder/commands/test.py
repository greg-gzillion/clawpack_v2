def run(args):
    """Run tests for code."""
    if not args:
        return "Usage: /test python exports/myfile.py\n       /test rust\n       /test go ./..."
    
    import subprocess
    from pathlib import Path
    
    parts = args.split()
    lang = parts[0].lower()
    target = parts[1] if len(parts) > 1 else ""
    
    test_commands = {
        "python": ["python", "-m", "pytest", str(Path("exports") / target), "-v"] if target else ["python", "-m", "pytest", "-v"],
        "rust": ["cargo", "test"],
        "go": ["go", "test", "./..."],
        "javascript": ["npx", "jest"],
        "typescript": ["npx", "jest"],
    }
    
    cmd = test_commands.get(lang)
    if not cmd:
        return f"Test runner not configured for '{lang}'. Supported: python, rust, go, javascript, typescript"
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.stdout.strip() or result.stderr.strip()
    except FileNotFoundError:
        return f"Test runner for {lang} not installed"
    except Exception as e:
        return f"Error: {e}"