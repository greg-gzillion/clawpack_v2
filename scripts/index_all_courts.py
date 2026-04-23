#!/usr/bin/env python3
"""Index all court markdown files into chronicle"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path.cwd()))

from agents.webclaw.core.chronicle_ledger import get_chronicle

def index_court_files():
    chronicle = get_chronicle()
    
    jurisdictions_path = Path("agents/webclaw/references/lawclaw/jurisdictions")
    
    if not jurisdictions_path.exists():
        print(f"❌ Path not found: {jurisdictions_path}")
        return
    
    # Find all markdown files
    md_files = list(jurisdictions_path.rglob("*.md"))
    total = len(md_files)
    print(f"📚 Found {total} court markdown files to index...")
    
    indexed = 0
    errors = 0
    
    for i, md_file in enumerate(md_files, 1):
        try:
            # Read content
            content = md_file.read_text(encoding='utf-8', errors='ignore')
            
            # Get relative path for source
            rel_path = md_file.relative_to(jurisdictions_path)
            source = f"lawclaw/jurisdictions/{rel_path.parent.name}"
            
            # Extract court name from filename or path
            court_name = md_file.stem.replace('_', ' ').title()
            county_name = rel_path.parent.name
            
            # Create context
            context = f"Court: {county_name} - {court_name}\n"
            
            # Extract key info for better search
            if 'Phone:' in content:
                import re
                phone_match = re.search(r'Phone[:\s]+([^\n]+)', content)
                if phone_match:
                    context += f"Phone: {phone_match.group(1)}\n"
            
            # Index the file
            chronicle.record_fetch(
                url=f"file://{md_file.absolute()}",
                context=context + content,
                source=source,
                metadata={
                    'county': county_name,
                    'court_type': court_name,
                    'path': str(md_file)
                }
            )
            indexed += 1
            
            # Progress indicator
            if i % 100 == 0:
                print(f"  Progress: {i}/{total} ({indexed} indexed, {errors} errors)")
                
        except Exception as e:
            errors += 1
            if errors <= 10:
                print(f"  ❌ Error indexing {md_file.name}: {e}")
    
    print(f"\n✅ Done! Indexed {indexed} of {total} files")
    print(f"⚠️ Errors: {errors}")
    
    # Show stats
    stats = chronicle.get_stats()
    print(f"\n📊 Updated Chronicle Stats:")
    print(f"   Total cards: {stats['total_cards']}")
    print(f"   Unique URLs: {stats['unique_urls']}")
    print(f"   Categories: {len(stats['sources'])}")

if __name__ == "__main__":
    index_court_files()
