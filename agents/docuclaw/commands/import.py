"""Import document command"""
name = "/import"

def run(args):
    if not args:
        print("Usage: /import <filename>")
        print("Supported formats: .txt, .md, .json, .csv, .html, .xml, .docx, .pdf, .rtf, .odt")
        return
    
    from pathlib import Path
    from importers.text import TextImporter
    from importers.markdown import MarkdownImporter
    from importers.json import JSONImporter
    from importers.csv import CSVImporter
    from importers.html import HTMLImporter
    from importers.xml import XMLImporter
    from importers.docx import DocxImporter
    from importers.pdf import PDFImporter
    from importers.rtf import RTFImporter
    from importers.odt import ODTImporter
    
    file_path = Path(args)
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return
    
    ext = file_path.suffix.lower()
    
    # Map extensions to importers
    importers = {
        ".txt": TextImporter(), ".text": TextImporter(), ".log": TextImporter(),
        ".md": MarkdownImporter(), ".markdown": MarkdownImporter(),
        ".json": JSONImporter(),
        ".csv": CSVImporter(), ".tsv": CSVImporter(),
        ".html": HTMLImporter(), ".htm": HTMLImporter(),
        ".xml": XMLImporter(),
        ".docx": DocxImporter(),
        ".pdf": PDFImporter(),
        ".rtf": RTFImporter(),
        ".odt": ODTImporter()
    }
    
    importer = importers.get(ext)
    if not importer:
        print(f"❌ Unsupported format: {ext}")
        print("💡 Supported: .txt, .md, .json, .csv, .html, .xml, .docx, .pdf, .rtf, .odt")
        return
    
    print(f"\n📥 Importing {file_path.name}...")
    result = importer.import_file(file_path)
    
    print(f"\n✅ Imported as {result.get('format', 'unknown')}")
    print(f"   Text length: {len(result.get('text', ''))} characters")
    
    # Show preview
    text = result.get('text', '')
    if text:
        print(f"\n--- Preview ---")
        print(text[:500])
        if len(text) > 500:
            print("\n... (truncated)")
    
    # Save imported content
    output_path = file_path.parent / f"imported_{file_path.stem}.md"
    output_path.write_text(f"# Imported from {file_path.name}\n\n{text}")
    print(f"\n💾 Saved to: {output_path}")
