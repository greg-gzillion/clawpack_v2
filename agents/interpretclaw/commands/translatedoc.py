"""Translate an entire document using modular translator"""
name = "/translatedoc"

def run(args):
    if not args:
        print("Usage: /translatedoc <file> <target_lang>")
        print("Example: /translatedoc mydoc.pdf es")
        return
    
    parts = args.split(" ", 1)
    if len(parts) < 2:
        print("Need file path and target language")
        return
    
    file_path = parts[0]
    target_lang = parts[1].lower()
    
    from pathlib import Path
    from core.config import SUPPORTED_LANGUAGES
    
    p = Path(file_path)
    if not p.exists():
        print(f"❌ File not found: {file_path}")
        return
    
    if target_lang not in SUPPORTED_LANGUAGES:
        print(f"Language '{target_lang}' not supported")
        return
    
    print(f"\n📄 Translating document: {p.name}")
    print(f"   Target language: {SUPPORTED_LANGUAGES[target_lang]}")
    
    # Use modular translator
    from translator import Translator
    translator = Translator()
    result = translator.translate_document(p, target_lang)
    
    if result.success:
        print(f"\n✅ Translation complete!")
        print(f"   {result.summary()}")
        print(f"   Chunks processed: {result.chunks_processed}")
    else:
        print(f"\n❌ Failed: {result.error}")
        print("\n💡 Make sure WebClaw is running for AI translation:")
        print("   python agents/webclaw/webclaw_agent.py")
