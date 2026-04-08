"""Analyze code statistics"""
name="/codestats"

def run(args):
    from pathlib import Path
    
    directory = args if args else "."
    search_dir = Path(directory)
    
    if not search_dir.exists():
        print(f"❌ Directory not found: {directory}")
        return
    
    code_extensions = {
        '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
        '.java': 'Java', '.c': 'C', '.cpp': 'C++', '.rs': 'Rust',
        '.go': 'Go', '.html': 'HTML', '.css': 'CSS', '.json': 'JSON'
    }
    
    stats = {}
    total_lines = 0
    total_files = 0
    
    for ext, lang in code_extensions.items():
        files = list(search_dir.rglob(f"*{ext}"))
        if files:
            lines = 0
            for f in files:
                try:
                    lines += len(f.read_text(encoding='utf-8', errors='ignore').split('\n'))
                except:
                    pass
            stats[lang] = {"files": len(files), "lines": lines}
            total_files += len(files)
            total_lines += lines
    
    print(f"\n📊 CODE STATISTICS for {search_dir.absolute()}\n")
    print(f"{'Language':<15} {'Files':<10} {'Lines':<10}")
    print("-" * 35)
    for lang, data in sorted(stats.items()):
        print(f"{lang:<15} {data['files']:<10} {data['lines']:<10,}")
    print("-" * 35)
    print(f"{'TOTAL':<15} {total_files:<10} {total_lines:<10,}")
