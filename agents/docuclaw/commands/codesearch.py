"""Search code across files"""
name = "/codesearch"

def run(args):
    if not args:
        print("Usage: /codesearch <pattern> [directory]")
        return
    
    from pathlib import Path
    import re
    
    parts = args.split()
    pattern = parts[0]
    directory = parts[1] if len(parts) > 1 else "."
    
    search_dir = Path(directory)
    if not search_dir.exists():
        print(f"❌ Directory not found: {directory}")
        return
    
    code_extensions = {'.py', '.js', '.java', '.c', '.cpp', '.h', '.rs', '.go', '.ts', '.jsx', '.tsx'}
    
    print(f"\n🔍 Searching for '{pattern}' in {search_dir}...\n")
    
    matches = []
    for file in search_dir.rglob("*"):
        if file.suffix in code_extensions:
            try:
                content = file.read_text(encoding='utf-8', errors='ignore')
                if re.search(pattern, content, re.IGNORECASE):
                    matches.append(file)
            except:
                pass
    
    if matches:
        print(f"✅ Found {len(matches)} matches:\n")
        for m in matches[:20]:
            print(f"  📄 {m.relative_to(search_dir)}")
    else:
        print("❌ No matches found")
