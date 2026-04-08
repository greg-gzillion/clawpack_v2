"""Export document command"""
name = "/export"
def run(args):
    if not args:
        print("Usage: /export <filename> [pdf|docx|html|txt]")
        return
    parts = args.split()
    file_path = parts[0]
    format_type = parts[1] if len(parts) > 1 else "txt"
    from pathlib import Path
    p = Path(file_path)
    if not p.exists():
        print(f"File not found: {file_path}")
        return
    content = p.read_text()
    output = p.parent / f"{p.stem}.{format_type}"
    output.write_text(content)
    print(f"✅ Exported to: {output}")
