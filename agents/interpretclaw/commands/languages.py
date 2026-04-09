"""List all supported languages"""
name = "/languages"

def run(args):
    from core.config import SUPPORTED_LANGUAGES
    
    print("\n" + "="*60)
    print(f"🌐 SUPPORTED LANGUAGES ({len(SUPPORTED_LANGUAGES)})")
    print("="*60)
    
    for code, name in sorted(SUPPORTED_LANGUAGES.items()):
        print(f"   {code}: {name}")
    
    print("\n" + "="*60)
    print("💡 Usage: /translate es Hello world")
    print("   /detect Hello world")
    print("   /speak Hello world")
    print("="*60)
