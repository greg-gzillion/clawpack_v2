"""Cache statistics and management command"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.cache import get_cache

def cache_stats_command(args=None):
    """Show cache statistics or clear cache"""
    
    cache = get_cache()
    stats = cache.stats()
    
    print("\n" + "="*50)
    print("📦 CACHE STATISTICS")
    print("="*50)
    print(f"Entries: {stats['entries']}")
    print(f"Total hits: {stats['total_hits']}")
    print(f"Average hits per entry: {stats['avg_hits']:.1f}")
    print("="*50)
    
    if args and args.lower() == "clear":
        confirm = input("\n⚠️  Clear entire cache? (y/N): ")
        if confirm.lower() == 'y':
            cache.clear()
            print("✅ Cache cleared")
    
    print("\n💡 Use '/cache clear' to clear the cache")

name = "/cache"
run = cache_stats_command
