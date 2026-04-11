"""Print to printer command (Windows)"""
name = "/print"

def run(args):
    if not args:
        print("Usage: /print <filename> [printer_name]")
        print("Example: /print mydoc.pdf")
        print("Example: /print mydoc.docx \"HP LaserJet\"")
        return
    
    from pathlib import Path
    import subprocess
    import tempfile
    
    parts = args.split()
    source = parts[0]
    printer = parts[1] if len(parts) > 1 else None
    
    p = Path(source)
    if not p.exists():
        print(f"❌ File not found: {source}")
        return
    
    print(f"\n🖨️ Sending {p.name} to printer...")
    
    # For .txt files, use Notepad to print
    if p.suffix.lower() == '.txt':
        try:
            if printer:
                subprocess.run(['notepad', '/p', str(p)], check=True)
            else:
                subprocess.run(['notepad', '/p', str(p)], check=True)
            print(f"✅ Sent to printer")
        except Exception as e:
            print(f"❌ Print error: {e}")
            print("💡 Make sure you have a default printer configured")
    
    # For .md files, convert to temp .txt first
    elif p.suffix.lower() == '.md':
        try:
            content = p.read_text(encoding='utf-8', errors='ignore')
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
                tmp.write(content)
                tmp_path = tmp.name
            subprocess.run(['notepad', '/p', tmp_path], check=True)
            print(f"✅ Sent to printer")
        except Exception as e:
            print(f"❌ Print error: {e}")
    
    else:
        print(f"⚠️ Printing {p.suffix} files may require external application")
        print("💡 Try converting to PDF first with /export")
