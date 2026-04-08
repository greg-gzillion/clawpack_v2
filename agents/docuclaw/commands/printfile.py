"""Print to file command"""
name = "/printfile"

def run(args):
    if not args:
        print("Usage: /printfile <filename> [output_filename]")
        print("Example: /printfile mydoc.md printed_copy.txt")
        return
    
    from pathlib import Path
    parts = args.split()
    source = parts[0]
    output = parts[1] if len(parts) > 1 else f"printed_{Path(source).stem}.txt"
    
    p = Path(source)
    if not p.exists():
        print(f"❌ File not found: {source}")
        return
    
    content = p.read_text(encoding='utf-8', errors='ignore')
    out_path = Path(output)
    
    # Add print formatting
    formatted = f"""
{'='*60}
PRINTED FROM DOCUCLAW
{'='*60}
File: {p.name}
Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

{content}

{'='*60}
End of document
{'='*60}
"""
    out_path.write_text(formatted, encoding='utf-8')
    print(f"✅ Printed to file: {out_path.absolute()}")
