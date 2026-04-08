"""Compare two code files"""
name = "/diff"

def run(args):
    if not args:
        print("Usage: /diff <file1> <file2>")
        return
    
    parts = args.split()
    if len(parts) < 2:
        print("❌ Need two files to compare")
        return
    
    from pathlib import Path
    import difflib
    
    p1 = Path(parts[0])
    p2 = Path(parts[1])
    
    if not p1.exists() or not p2.exists():
        print("❌ One or both files not found")
        return
    
    content1 = p1.read_text(encoding='utf-8', errors='ignore').splitlines()
    content2 = p2.read_text(encoding='utf-8', errors='ignore').splitlines()
    
    diff = difflib.unified_diff(content1, content2, fromfile=str(p1), tofile=str(p2), lineterm='')
    
    print(f"\n🔍 DIFF: {p1.name} vs {p2.name}\n")
    for line in diff:
        if line.startswith('+'):
            print(f"\033[92m{line}\033[0m")  # Green for additions
        elif line.startswith('-'):
            print(f"\033[91m{line}\033[0m")  # Red for deletions
        elif line.startswith('@@'):
            print(f"\033[93m{line}\033[0m")  # Yellow for headers
        else:
            print(line)
