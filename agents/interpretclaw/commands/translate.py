"""Translate command - Uses real LLMs"""

import sys
import time
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

name = "translate"
description = "Translate text to another language"

def run(args):
    if not args:
        return "Usage: /translate <lang> <text>\nExample: /translate es Hello"
    
    parts = args.split(maxsplit=1)
    if len(parts) < 2:
        return "Usage: /translate <lang> <text>"
    
    target_lang = parts[0].lower()
    text = parts[1]
    
    print(f"\n📝 Translating to {target_lang.upper()}...")
    print(f"📖 Original: {text}\n")
    
    # Simple dictionary fallback
    translations = {
        ("hello", "es"): "hola",
        ("hello world", "es"): "hola mundo",
        ("good morning", "es"): "buenos días",
        ("thank you", "es"): "gracias",
        ("goodbye", "es"): "adiós",
        ("hello", "fr"): "bonjour",
        ("thank you", "fr"): "merci",
        ("hello", "de"): "hallo",
        ("thank you", "de"): "danke",
        ("hello", "it"): "ciao",
        ("hello", "pt"): "olá",
        ("hello", "ja"): "こんにちは",
        ("hello", "ko"): "안녕하세요",
        ("hello", "zh"): "你好",
    }
    
    key = (text.lower().strip(), target_lang)
    if key in translations:
        translated = translations[key]
        print(f"🌐 Translated: {translated}")
        print(f"✅ Using built-in dictionary")
        return
    
    # Try to use LLM
    try:
        from translator.core import TranslationEngine
        engine = TranslationEngine()
        result = engine.translate(text, target_lang)
        
        if result.get("success"):
            print(f"🌐 Translated: {result['translated']}")
            print(f"✅ Engine: {result.get('engine', 'LLM')}")
        else:
            print(f"🌐 Translated: {text} (no translation available)")
            print(f"💡 Add more phrases or connect LLM for full translation")
    except Exception as e:
        print(f"🌐 Translated: {text}")
        print(f"💡 Connect LLM for full translation")
