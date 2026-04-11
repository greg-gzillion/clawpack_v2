def run(args):
    """Medical research using chronicle index"""
    if not args:
        return "Usage: /med <condition>\nExample: /med cardiology"
    
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from shared.chronicle_helper import search_chronicle
    
    results = search_chronicle(args)
    if not results:
        return f"No medical info found for '{args}'\nTry: /chronicle search {args}"
    
    output = [f"🏥 MEDICAL: {args}\n"]
    for card in results[:5]:
        output.append(f"🔗 {card.url}")
    return "\n".join(output)
