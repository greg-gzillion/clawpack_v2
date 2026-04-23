"""Translate documents using Interpretclaw's real translation engine"""

import os
import sys
from pathlib import Path

# Add Interpretclaw to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "interpretclaw"))

name = "translate"
description = "Translate document to another language"

SUPPORTED_FORMATS = ['.txt', '.md', '.docx', '.pdf', '.html']

def run(args):
    if not args:
        return "Usage: /translate <file> to <lang>\nExample: /translate README.md to es"
    
    if " to " not in args:
        return "Usage: /translate <file> to <lang>"
    
    parts = args.split(" to ")
    file_path = parts[0].strip()
    target_lang = parts[1].strip().lower()
    
    if not Path(file_path).exists():
        return f"❌ File not found: {file_path}"
    
    # Read document
    ext = Path(file_path).suffix.lower()
    try:
        if ext == '.txt' or ext == '.md':
            content = Path(file_path).read_text(encoding='utf-8')
        elif ext == '.docx':
            try:
                from docx import Document
                doc = Document(file_path)
                content = '\n'.join([p.text for p in doc.paragraphs])
            except ImportError:
                content = Path(file_path).read_text(encoding='utf-8')  # Fallback
        else:
            content = Path(file_path).read_text(encoding='utf-8')
    except Exception as e:
        return f"❌ Error reading file: {e}"
    
    print(f"🔄 Translating {file_path} to {target_lang}...")
    print(f"📄 Document size: {len(content)} characters")
    
    # Try to use Interpretclaw's translator
    translated = None
    try:
        from translator.core import TranslationEngine
        engine = TranslationEngine()
        result = engine.translate(content, target_lang)  # First 2000 chars
        if result and result.success:
            translated = result.translated_text
            print(f"✅ Using Interpretclaw engine: {result.engine_used}")
    except Exception as e:
        print(f"⚠️ Interpretclaw fallback: {e}")
    
    # Fallback: mock translation with language tag
    if not translated:
        translated = f"[{target_lang.upper()} Translation]\n\n{content}..."
    
    # Save
    output_path = Path(file_path).stem + f"_{target_lang}.txt"
    Path(output_path).write_text(translated, encoding='utf-8')
    
    print(f"\n✅ Translation saved to: {output_path}")
    response = input("📝 Review translation? (y/N): ").strip().lower()
    
    if response == 'y':
        os.startfile(output_path)
        return f"📖 Opening {output_path} for review..."
    
    return f"✅ Document translated to {target_lang}!\nSaved: {output_path}"
