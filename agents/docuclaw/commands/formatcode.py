"""Auto-format code files"""
name = "/formatcode"

def run(args):
    if not args:
        print("Usage: /formatcode <filename>")
        return
    
    from pathlib import Path
    
    p = Path(args)
    if not p.exists():
        print(f"❌ File not found: {p}")
        return
    
    content = p.read_text(encoding='utf-8', errors='ignore')
    ext = p.suffix.lower()
    
    formatted = content
    
    # Simple Python formatting
    if ext == '.py':
        lines = content.split('\n')
        formatted_lines = []
        indent_level = 0
        for line in lines:
            stripped = line.strip()
            if stripped.endswith(':'):
                formatted_lines.append('    ' * indent_level + stripped)
                indent_level += 1
            elif stripped == '':
                formatted_lines.append('')
            else:
                formatted_lines.append('    ' * indent_level + stripped)
        formatted = '\n'.join(formatted_lines)
    
    output = p.parent / f"formatted_{p.name}"
    output.write_text(formatted)
    print(f"✅ Formatted code saved to: {output}")
