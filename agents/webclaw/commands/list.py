"""List available web/cloud categories"""

def list_command(args=None):
    from core.config import WEB_REFS
    
    print("\n" + "="*50)
    print("📋 WEBCLAW CATEGORIES")
    print("="*50)
    
    if WEB_REFS.exists():
        categories = sorted([d.name for d in WEB_REFS.iterdir() if d.is_dir()])
        
        # Display in columns
        for i, cat in enumerate(categories):
            if i % 4 == 0 and i > 0:
                print()
            print(f"  {cat:<25}", end="")
    
    print("\n" + "="*50)
    print("💡 Use /browse [category] to explore")
    print("   Use /search [term] to find specific content")
