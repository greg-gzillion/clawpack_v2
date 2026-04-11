def run(args):
    """Data references from chronicle"""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from shared.chronicle_helper import search_chronicle
    
    results = search_chronicle(args)
    if results:
        return f"📊 DATA REFERENCES for '{args}':\n" + "\n".join([f"  • {c.url}" for c in results[:3]])
    return f"Data: {args}\n(No references found)"
