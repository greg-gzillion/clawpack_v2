"""Chronicle commands - URL context recovery and timeline"""
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.chronicle_ledger import get_chronicle

def run(args):
    chronicle = get_chronicle()
    
    if not args:
        stats = chronicle.get_stats()
        return f"Chronicle: {stats['total_cards']} cards, {stats['unique_urls']} unique URLs"
    
    parts = args.split(maxsplit=1)
    cmd = parts[0].lower()
    query = parts[1] if len(parts) > 1 else ""
    
    if cmd == "stats":
        stats = chronicle.get_stats()
        return f"Cards: {stats['total_cards']}\nUnique URLs: {stats['unique_urls']}\nSources: {stats['sources']}"
    
    elif cmd == "timeline":
        timeline = chronicle.get_timeline()
        if not timeline:
            return "No cards in ledger yet"
        output = ["📅 Timeline (most recent):"]
        for card in timeline[:5]:
            output.append(f"  • {card.url[:60]}... ({card.timestamp[:19]})")
        return "\n".join(output)
    
    elif cmd == "search":
        if not query:
            return "Usage: /chronicle search <query>"
        results = chronicle.recover_by_context(query)
        if not results:
            return f"No results for '{query}'"
        output = [f"🔍 Results for '{query}':"]
        for card in results:
            output.append(f"  • {card.url}")
        return "\n".join(output)
    
    return "Unknown chronicle command. Use stats, timeline, or search"
