"""Batch print multiple files"""
name = "/batchprint"

def run(args):
    if not args:
        print("Usage: /batchprint <folder>")
        print("Example: /batchprint ./documents")
        return
    
    from pathlib import Path
    
    folder = Path(args)
    if not folder.exists() or not folder.is_dir():
        print(f"❌ Folder not found: {folder}")
        return
    
    files = list(folder.glob("*.md")) + list(folder.glob("*.txt")) + list(folder.glob("*.docx"))
    
    if not files:
        print(f"No printable files found in {folder}")
        return
    
    print(f"\n🖨️ Printing {len(files)} files from {folder}...")
    
    for f in files:
        print(f"  Printing: {f.name}")
        # Use the print command for each file
        from commands.print import run as print_run
        print_run(str(f))
    
    print(f"\n✅ Batch print complete")
