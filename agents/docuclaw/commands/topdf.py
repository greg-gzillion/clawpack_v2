"""Convert to PDF command"""
name = "/topdf"

def run(args):
    if not args:
        print("Usage: /topdf <filename>")
        print("Example: /topdf mydocument.md")
        return
    
    from pathlib import Path
    import subprocess
    
    source = args
    p = Path(source)
    if not p.exists():
        print(f"❌ File not found: {source}")
        return
    
    output = p.parent / f"{p.stem}.pdf"
    
    print(f"\n📄 Converting {p.name} to PDF...")
    
    # For .md files, convert to HTML first then PDF (simplified)
    if p.suffix.lower() == '.md':
        try:
            content = p.read_text(encoding='utf-8', errors='ignore')
            html_content = f"<html><body><pre>{content}</pre></body></html>"
            html_path = p.parent / f"{p.stem}.html"
            html_path.write_text(html_content)
            
            # Try to use browser to print to PDF
            import webbrowser
            webbrowser.open(str(html_path.absolute()))
            print(f"✅ Opening {html_path} in browser - use Ctrl+P to save as PDF")
            print(f"   File will be saved as: {output}")
        except Exception as e:
            print(f"❌ Conversion error: {e}")
    else:
        print(f"💡 Use /export {source} pdf to create PDF")
