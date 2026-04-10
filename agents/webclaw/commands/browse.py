"""Browse web/cloud categories"""

def browse_command(args=None):
    from core.config import WEB_REFS
    
    if not args:
        print("Usage: /browse [category]")
        print("   Use /list to see all categories")
        return
    
    category_path = WEB_REFS / args
    if not category_path.exists():
        print(f"Category '{args}' not found")
        print("Use /list to see available categories")
        return
    
    print(f"\n📁 BROWSING: {args.upper()}\n")
    
    # Count files
    md_files = list(category_path.rglob("*.md"))
    print(f"📄 Files: {len(md_files)}\n")
    
    # Show first 20 files
    for i, f in enumerate(md_files[:20], 1):
        rel_path = f.relative_to(category_path)
        print(f"  {i:2}. {rel_path}")
    
    if len(md_files) > 20:
        print(f"\n  ... and {len(md_files) - 20} more files")
    
    print(f"\n💡 Use /search [term] to search within {args}")
