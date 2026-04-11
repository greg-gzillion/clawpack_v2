"""Syntax highlighting for code files"""
name = "/highlight"

def run(args):
    if not args:
        print("Usage: /highlight <filename>")
        return
    
    from pathlib import Path
    import re
    
    p = Path(args)
    if not p.exists():
        print(f"❌ File not found: {p}")
        return
    
    content = p.read_text(encoding='utf-8', errors='ignore')
    ext = p.suffix.lower()
    
    # Simple ANSI color highlighting
    colors = {
        "keyword": "\033[94m",    # Blue
        "string": "\033[92m",     # Green
        "comment": "\033[90m",    # Dark Gray
        "number": "\033[95m",     # Magenta
        "function": "\033[93m",   # Yellow
        "reset": "\033[0m"
    }
    
    # Language-specific keyword lists
    keywords = {
        ".py": ["def", "class", "import", "from", "if", "else", "for", "while", "return", "True", "False", "None"],
        ".js": ["function", "const", "let", "var", "if", "else", "return", "class", "import", "export"],
        ".java": ["public", "private", "class", "static", "void", "int", "String", "if", "else", "return"],
        ".c": ["int", "char", "void", "return", "if", "else", "for", "while", "struct", "typedef"],
        ".cpp": ["int", "char", "void", "class", "public", "private", "virtual", "return", "if", "else"],
        ".rs": ["fn", "let", "mut", "pub", "impl", "trait", "use", "mod", "if", "else", "match", "return"],
        ".go": ["func", "var", "const", "type", "struct", "interface", "if", "else", "for", "return", "package", "import"]
    }
    
    lang_keywords = keywords.get(ext, ["if", "else", "return", "for", "while"])
    
    # Apply highlighting
    highlighted = content
    for kw in lang_keywords:
        highlighted = re.sub(fr'\b{kw}\b', f"{colors['keyword']}{kw}{colors['reset']}", highlighted)
    
    # Highlight strings
    highlighted = re.sub(r'(".*?")', f"{colors['string']}\\1{colors['reset']}", highlighted)
    highlighted = re.sub(r"('.*?')", f"{colors['string']}\\1{colors['reset']}", highlighted)
    
    # Highlight comments
    highlighted = re.sub(r'(#.*?$)', f"{colors['comment']}\\1{colors['reset']}", highlighted, flags=re.MULTILINE)
    
    print(f"\n🎨 Syntax Highlighted: {p.name}\n")
    print(highlighted[:5000])
    if len(highlighted) > 5000:
        print("\n... (truncated)")
