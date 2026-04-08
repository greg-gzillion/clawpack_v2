"""Search web/cloud references"""

def search_command(args=None):
    if not args:
        print("Usage: /search [term]")
        return
    
    from core.config import WEB_REFS
    import re
    
    print(f"\n🔍 Searching for: {args}\n")
    
    results = []
    if WEB_REFS.exists():
        for category in WEB_REFS.iterdir():
            if category.is_dir():
                for md_file in category.rglob("*.md"):
                    try:
                        content = md_file.read_text(encoding='utf-8', errors='ignore')
                        if args.lower() in content.lower():
                            results.append({
                                "file": md_file.name,
                                "category": category.name,
                                "preview": content[:300]
                            })
                            if len(results) >= 10:
                                break
                    except:
                        pass
            if len(results) >= 10:
                break
    
    if results:
        print(f"✅ Found {len(results)} results:\n")
        for r in results:
            print(f"  📁 {r['category']}/{r['file']}")
            print(f"     {r['preview'][:150]}...\n")
    else:
        print("❌ No results found")
