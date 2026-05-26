"""Index ALL jurisdiction file content into Chronicle for cross-agent full-text search.

Every municipal_court.md and law_resources.md gets its FULL content indexed,
not just URLs. Courts, police, jails, hospitals, libraries, building permits —
everything searchable by every agent.
"""
import sys
import json
import re
import hashlib
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from agents.webclaw.core.chronicle_ledger import get_chronicle

JURISDICTIONS_ROOT = PROJECT_ROOT / "agents" / "webclaw" / "references" / "lawclaw" / "jurisdictions" / "us"

def extract_metadata(filepath: Path, content: str) -> dict:
    """Extract rich metadata from a jurisdiction file."""
    parts = filepath.parts
    state = county = city = "unknown"
    for i, part in enumerate(parts):
        if part == "us" and i + 1 < len(parts):
            state = parts[i + 1]
        if part == state and i + 1 < len(parts):
            county = parts[i + 1]
        if part == county and i + 1 < len(parts):
            city = parts[i + 1]

    urls = list(set(re.findall(r'https?://[^\s\)\]\<\>\"]+', content)))
    
    coords = re.findall(r'(?:Latitude|Longitude)[:\s]*([-\d.]+)', content)
    lat = coords[0] if len(coords) > 0 else None
    lon = coords[1] if len(coords) > 1 else None

    phones = list(set(re.findall(r'\(?\d{3}\)?[\s-]*\d{3}[\s-]*\d{4}', content)))

    sections = {}
    current_section = "preamble"
    current_lines = []
    for line in content.split('\n'):
        if line.startswith('## '):
            if current_lines:
                sections[current_section] = '\n'.join(current_lines).strip()
            current_section = line[3:].strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_lines:
        sections[current_section] = '\n'.join(current_lines).strip()

    return {
        'state': state,
        'county': county,
        'city': city,
        'file_type': filepath.stem,
        'urls': urls,
        'url_count': len(urls),
        'coordinates': {'lat': lat, 'lon': lon} if lat and lon else None,
        'phone_numbers': phones[:20],
        'sections': list(sections.keys()),
        'content_size': len(content),
    }

def main():
    chronicle = get_chronicle()
    files = list(JURISDICTIONS_ROOT.rglob("*.md"))
    
    skip_patterns = ['design_resources', 'docu_resources', 'draw_resources', 
                     'medi_resources', 'state_law', 'federal', 'supreme_court', 
                     'constitution', '__pycache__']
    files = [f for f in files if not any(p in str(f) for p in skip_patterns)]
    
    print(f"Indexing {len(files)} files with FULL content into Chronicle...")
    print(f"Target: Every court, police dept, jail, hospital, library, building permit detail searchable\n")
    
    indexed = 0
    skipped = 0
    errors = 0
    total_size = 0
    
    for filepath in files:
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
            if not content.strip():
                skipped += 1
                continue
            
            meta = extract_metadata(filepath, content)
            total_size += meta['content_size']
            
            # Build rich context with full content - NO truncation
            context = f"""STATE: {meta['state']} | COUNTY: {meta['county']} | CITY: {meta['city']}
FILE: {meta['file_type']}
PATH: {filepath}
PHONES: {' | '.join(meta['phone_numbers'][:10])}
URLS: {' | '.join(meta['urls'][:20])}
COORDINATES: lat={meta['coordinates']['lat'] if meta['coordinates'] else 'N/A'} lon={meta['coordinates']['lon'] if meta['coordinates'] else 'N/A'}
SECTIONS: {' | '.join(meta['sections'])}
---
{content}
"""
            
            url = f"jurisdiction://{meta['state']}/{meta['county']}/{meta['city']}/{meta['file_type']}"
            
            chronicle.record_fetch(
                url=url,
                context=context,
                source=f"jurisdiction:{meta['state']}",
                metadata={
                    'state': meta['state'],
                    'county': meta['county'],
                    'city': meta['city'],
                    'file_type': meta['file_type'],
                    'coordinates': meta['coordinates'],
                    'url_count': meta['url_count'],
                    'phone_count': len(meta['phone_numbers']),
                    'content_size': meta['content_size'],
                    'sections': meta['sections'],
                }
            )
            indexed += 1
            
            if indexed % 2000 == 0:
                print(f"  Indexed: {indexed} | Size: {total_size/1024/1024:.1f}MB | Skipped: {skipped} | Errors: {errors}")
                
        except Exception as e:
            errors += 1
            if errors <= 20:
                print(f"  Error [{filepath.name}]: {str(e)[:100]}")
    
    print(f"\n{'='*60}")
    print(f"INDEXING COMPLETE")
    print(f"  Files indexed: {indexed}")
    print(f"  Skipped (empty): {skipped}")
    print(f"  Errors: {errors}")
    print(f"  Total content: {total_size/1024/1024:.1f}MB")
    print(f"  Estimated Chronicle entries: ~{35177 + indexed}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
