"""Translation search for PolyClaw"""

from core.data import get_data_path
import json

def translate_command(text):
    if not text:
        print("Usage: /translate 'hello'")
        return
    
    print(f"\n🌐 Translation requested: {text}")
    print("Note: Full translation requires API key. Basic mode active.")
    print("To enable full translation, add API key to config.")
    
    # Basic word lookup from reference files
    data_path = get_data_path()
    for md_file in data_path.glob("**/*.md"):
        try:
            content = md_file.read_text(encoding='utf-8', errors='ignore')
            if text.lower() in content.lower():
                print(f"\n📚 Found in: {md_file.name}")
                print("-"*40)
                # Show first 500 chars
                print(content[:500])
                if len(content) > 500:
                    print("\n... (more available)")
                return
        except:
            pass
    
    print("No translation found. Check language reference files.")

def languages_command(args=None):
    print("\n📚 Available language references:")
    data_path = get_data_path()
    for folder in data_path.iterdir():
        if folder.is_dir():
            print(f"  • {folder.name}")