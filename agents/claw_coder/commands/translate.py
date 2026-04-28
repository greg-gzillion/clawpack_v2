def run(args):
    """Translate code between languages. Usage: /translate python rust exports/myfile.py"""
    if not args:
        return "Usage: /translate python rust exports/myfile.py"

    from pathlib import Path

    parts = args.split()
    if len(parts) < 3:
        return "Usage: /translate python rust exports/myfile.py"

    from_lang = parts[0].lower()
    to_lang = parts[1].lower()
    target = parts[2]

    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
    EXPORTS = PROJECT_ROOT / "exports"

    filepath = EXPORTS / target if "/" not in target else Path(target)
    if not filepath.exists():
        return f"File not found: {filepath}"

    content = filepath.read_text(encoding="utf-8", errors="ignore")

    from agents.claw_coder.agent_handler import _agent
    
    result = _agent.ask_llm(
        f"Translate this {from_lang} code to idiomatic {to_lang}. "
        f"Keep the same functionality. Return only the translated code with brief comments.\n\n"
        f"Original {from_lang} code:\n{content[:4000]}"
    )

    # Save translated file
    from datetime import datetime
    base = filepath.stem
    ext_map = {"python": ".py", "rust": ".rs", "go": ".go", "javascript": ".js", 
               "typescript": ".ts", "java": ".java", "cpp": ".cpp", "c": ".c"}
    ext = ext_map.get(to_lang, ".txt")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_name = f"{base}_to_{to_lang}_{ts}{ext}"
    out_path = EXPORTS / out_name

    # Extract code from response if wrapped
    code = result
    if "```" in code:
        blocks = code.split("```")
        for i, block in enumerate(blocks):
            if i % 2 == 1:
                block = block.split("\n", 1)[1] if "\n" in block else block
                code = block
                break

    out_path.write_text(code, encoding="utf-8")

    # Validate the output if compiler available
    import subprocess
    validation = ""
    validators = {
        "python": ["python", "-m", "py_compile", str(out_path)],
        "rust": ["rustc", "--edition", "2024", "--emit=metadata", str(out_path)],
        "go": ["go", "fmt", str(out_path)],
        "javascript": ["node", "--check", str(out_path)],
    }
    if to_lang in validators:
        try:
            val_result = subprocess.run(validators[to_lang], capture_output=True, text=True, timeout=15)
            validation = f" | Validated: {'OK' if val_result.returncode == 0 else val_result.stderr[:100]}"
        except:
            validation = f" | Validator not installed for {to_lang}"

    return f"Translated {from_lang} -> {to_lang}\nSaved: {out_name}{validation}\n\n{result}"