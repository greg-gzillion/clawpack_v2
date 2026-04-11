#!/usr/bin/env python3
"""Index all reference URLs into chronicle ledger"""
import sys
from pathlib import Path
import re

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.webclaw.core.chronicle_ledger import get_chronicle

def extract_urls_from_md(file_path):
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        urls = re.findall(r'https?://[^\s<>"\')\]]+', content)
        return [url.rstrip('.,;:!?') for url in urls]
    except:
        return []

def main():
    print("📚 Indexing references into chronicle ledger...")
    chronicle = get_chronicle()
    references_dir = Path("agents/webclaw/references")
    
    if not references_dir.exists():
        print(f"Error: {references_dir} not found")
        return
    
    total = 0
    for md_file in references_dir.rglob("*.md"):
        category = str(md_file.relative_to(references_dir).parent)
        urls = extract_urls_from_md(md_file)
        for url in urls:
            chronicle.record_fetch(
                url=url,
                context=f"From {category}",
                source=category,
                metadata={"file": str(md_file)}
            )
            total += 1
            if total % 100 == 0:
                print(f"  Indexed {total} URLs...")
    
    print(f"\n✅ Indexed {total} URLs")
    stats = chronicle.get_stats()
    print(f"Total cards: {stats['total_cards']}")
    print(f"Unique URLs: {stats['unique_urls']}")

if __name__ == "__main__":
    main()
