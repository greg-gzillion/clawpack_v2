"""WebClaw statistics - shows reference database info"""

def stats_command(args=None):
    from core.config import WEB_REFS
    
    print("\n" + "="*50)
    print("🌐 WEBCLAW STATISTICS")
    print("="*50)
    
    if WEB_REFS.exists():
        # Count reference categories
        categories = [d for d in WEB_REFS.iterdir() if d.is_dir()]
        print(f"📚 Reference Categories: {len(categories)}")
        
        # Show top categories
        print("\n📁 Top Categories:")
        for cat in sorted(categories)[:10]:
            print(f"   • {cat.name}")
        if len(categories) > 10:
            print(f"   ... and {len(categories) - 10} more")
    
    print("="*50)
