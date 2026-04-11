"""Review and edit documents"""

import os
from pathlib import Path

name = "review"
description = "Open document for review"

def run(args):
    if not args:
        # List available documents
        docs = list(Path(".").glob("*.txt")) + list(Path(".").glob("*.md")) + list(Path(".").glob("*.docx"))
        if docs:
            return "📁 Available documents:\n" + "\n".join([f"  • {d.name}" for d in docs[:10]])
        return "No documents found. Use /translate to create translations."
    
    file_path = args.strip()
    if Path(file_path).exists():
        os.startfile(file_path)
        return f"📖 Opening {file_path} for review..."
    
    return f"❌ File not found: {file_path}"
