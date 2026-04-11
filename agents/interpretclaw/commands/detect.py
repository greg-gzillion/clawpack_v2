"""Detect language of text"""
name = "/detect"

def run(args):
    if not args:
        print("Usage: /detect <text>")
        return
    
    text = args.lower()
    
    # Simple word detection
    lang_words = {
        "hello": "en", "world": "en", "good": "en", "thank": "en",
        "hola": "es", "mundo": "es", "gracias": "es",
        "bonjour": "fr", "monde": "fr", "merci": "fr",
        "hallo": "de", "welt": "de", "danke": "de"
    }
    
    detected = "unknown"
    for word in text.split():
        if word in lang_words:
            detected = lang_words[word].upper()
            break
    
    from core.config import SUPPORTED_LANGUAGES
    lang_name = SUPPORTED_LANGUAGES.get(detected.lower(), "Unknown")
    
    print(f"\n🔍 Text: {args}")
    print(f"   Detected: {detected} ({lang_name})")
    print("\n💡 For accurate detection, ensure WebClaw is running")
