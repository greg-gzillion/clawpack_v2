"""Help command"""
name = "/help"
def run(args):
    print("\n" + "="*70)
    print("DOCUCLAW - ADVANCED DOCUMENT & CODE PROCESSOR")
    print("="*70)
    
    print("\n📥 IMPORT & EXPORT:")
    print("  /import <file>       - Import any document (txt, md, json, csv, html, xml, docx, pdf, rtf, odt)")
    print("  /export <file>       - Export to format (pdf, docx, html, txt)")
    print("  /exportapp <file> <app> - Open in Word, Excel, Browser, Email, Cloud")
    
    print("\n💻 CODE PROCESSING:")
    print("  /highlight <file>    - Syntax highlighting for code")
    print("  /formatcode <file>   - Auto-format code")
    print("  /diff <file1> <file2> - Compare two files")
    print("  /codesearch <pattern> - Search code across files")
    print("  /codestats [dir]     - Analyze code statistics")
    
    print("\n📄 DOCUMENT CREATION:")
    print("  /templates           - List all templates")
    print("  /create <template>   - Create document from template")
    print("  /analyze <file>      - Analyze document")
    
    print("\n🖨️ PRINTING:")
    print("  /printfile <file>    - Print to file")
    print("  /print <file>        - Print to printer")
    print("  /batchprint <folder> - Print all files in folder")
    print("  /topdf <file>        - Convert to PDF")
    
    print("\n📁 TEMPLATES:")
    print("  business/letter, business/meeting_minutes, business/proposal")
    print("  education/lesson_plan, education/research_paper")
    print("  technical/api_docs, technical/readme, technical/code_review")
    print("  personal/resume, personal/cover_letter, personal/todo")
    
    print("\n💡 TIPS:")
    print("  • Highlight code: /highlight app.py")
    print("  • Compare files: /diff old.py new.py")
    print("  • Search codebase: /codesearch TODO")
    print("  • Get code stats: /codestats ./src")
    print("="*70)
