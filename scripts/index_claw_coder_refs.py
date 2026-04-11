#!/usr/bin/env python3
"""Index all claw_coder references into the chronicle ledger"""
import sys
from pathlib import Path
import re

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.webclaw.core.chronicle_ledger import get_chronicle

def extract_urls_from_md(file_path: Path) -> list:
    """Extract URLs from markdown file"""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        urls = re.findall(r'https?://[^\s<>"\')\]]+', content)
        return [url.rstrip('.,;:!?') for url in urls]
    except:
        return []

def main():
    chronicle = get_chronicle()
    refs_dir = Path("agents/webclaw/references/claw_coder")
    
    if not refs_dir.exists():
        print(f"❌ Directory not found: {refs_dir}")
        return
    
    print(f"📚 Indexing claw_coder references into chronicle...")
    print("="*50)
    
    total_urls = 0
    total_files = 0
    
    for md_file in refs_dir.rglob("*.md"):
        if md_file.name == "README.md":
            continue
            
        language = md_file.parent.name
        urls = extract_urls_from_md(md_file)
        
        if urls:
            total_files += 1
            total_urls += len(urls)
            
            for url in urls:
                chronicle.record_fetch(
                    url=url,
                    context=f"Programming reference for {language}",
                    source=f"claw_coder/{language}",
                    metadata={"file": str(md_file), "language": language}
                )
            
            print(f"  ✓ {language}: {len(urls)} URLs indexed")
    
    print(f"\n✅ Indexed {total_urls} URLs from {total_files} language reference files")
    
    stats = chronicle.get_stats()
    print(f"\n📊 Chronicle Stats:")
    print(f"   Total cards: {stats['total_cards']}")
    print(f"   Unique URLs: {stats['unique_urls']}")
    print(f"   Categories: {len(stats['sources'])}")

if __name__ == "__main__":
    main()
