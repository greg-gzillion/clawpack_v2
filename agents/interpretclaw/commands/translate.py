"""Translate text between languages using modular translator"""
name = "/translate"

def run(args):
    if not args:
        print("Usage: /translate <lang> <text>")
        print("Example: /translate es Hello world")
        return
    
    parts = args.split(" ", 1)
    if len(parts) < 2:
        print("Need target language and text")
        return
    
    target_lang = parts[0].lower()
    text = parts[1]
    
    from core.config import SUPPORTED_LANGUAGES
    
    if target_lang not in SUPPORTED_LANGUAGES:
        print(f"Language '{target_lang}' not supported")
        print("Type /languages to see all 39 languages")
        return
    
    print(f"\n📝 Translating to {SUPPORTED_LANGUAGES[target_lang]}...")
    
    # Use modular translator
    from translator import Translator
    translator = Translator()
    result = translator.translate_text(text, target_lang)
    
    if result.success:
        print(f"\n📖 Original: {text}")
        print(f"\n🌐 Translated: {result.translated_text}")
        print(f"\n{result.summary()}")
    else:
        print(f"\n❌ Translation failed: {result.error}")
        print("\n💡 Start WebClaw for better translation:")
        print("   python agents/webclaw/webclaw_agent.py")
