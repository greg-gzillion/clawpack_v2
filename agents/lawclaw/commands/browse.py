"""browse command - Display jurisdiction files in CLI + open URLs in browser"""
import webbrowser
import re
from pathlib import Path

name = "/browse"

from agents.lawclaw.commands._memory import show_prior, remember


def run(args):
    if not args:
        return "[BROWSE] Usage: /browse [state] [county] [city] -- e.g., /browse MA, /browse MA Worcester, /browse MA Worcester Worcester"

    parts = args.strip().split()
    state = parts[0].upper() if len(parts) > 0 else ""
    county = parts[1] if len(parts) > 1 else ""
    city = parts[2] if len(parts) > 2 else ""

    if not state.isalpha() or len(state) != 2:
        return f"[ERROR] Invalid state code: {state}. Use 2-letter code like MA, TX, CA."

    output = []
    location_parts = [p for p in [city, county, state] if p]
    location_str = ", ".join(location_parts)
    
    output.append("")
    output.append(f"BROWSE: {location_str}")
    output.append("=" * 60)

    prior = show_prior(args, output)

    LAW_REFS = Path(__file__).parent.parent.parent.parent / "agents" / "webclaw" / "references" / "lawclaw"
    base = LAW_REFS / "jurisdictions" / "us" / state
    
    if county:
        base = base / county
    if city:
        base = base / city

    if not base.exists():
        output.append("")
        output.append(f"[EMPTY] No jurisdiction data found for {location_str}")
        output.append("[TIP] Try /list to see available states")
        output.append("[TIP] Try /search [query] to search all references")
        return "\n".join(output)

    md_files = list(base.glob("*.md"))
    if not city and county:
        for d in base.iterdir():
            if d.is_dir():
                md_files.extend(d.glob("*.md"))
    
    md_files = sorted(md_files)

    if not md_files:
        output.append("")
        output.append(f"[EMPTY] No reference files found for {location_str}")
        return "\n".join(output)

    output.append("")
    output.append(f"[DIR] Found {len(md_files)} reference files:")
    all_urls = []

    for f in md_files:
        rel_path = f.relative_to(LAW_REFS)
        output.append("")
        output.append("-" * 60)
        output.append(f"[FILE] {f.name} ({rel_path})")
        output.append("-" * 60)
        
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
            output.append(content[:2000])
            if len(content) > 2000:
                output.append("")
                output.append(f"... ({len(content) - 2000} more chars)")
            
            urls = re.findall(r'https?://[^\s\)\]\<\>\"]+', content)
            all_urls.extend(urls)
        except Exception as e:
            output.append(f"  Error reading: {e}")

    all_urls = list(set(all_urls))
    if all_urls:
        def url_score(url):
            score = 0
            url_lower = url.lower()
            if '.gov' in url_lower:
                score += 100
            if state.lower() in url_lower:
                score += 50
            if county and county.lower() in url_lower:
                score += 75
            if city and city.lower() in url_lower:
                score += 100
            if any(t in url_lower for t in ['court', 'judicial', 'supreme', 'appeals', 'municipal']):
                score += 25
            if any(t in url_lower for t in ['courtlistener', 'findlaw', 'justia', 'ballotpedia']):
                score -= 50
            return score
        
        ranked = sorted(all_urls, key=url_score, reverse=True)
        
        output.append("")
        output.append("=" * 60)
        output.append(f"[URL] OFFICIAL URLS ({len(ranked)}):")
        for i, url in enumerate(ranked[:10], 1):
            output.append(f"  [{i}] {url}")
        
        best_url = ranked[0]
        for url in ranked[:5]:
            try:
                import requests as req
                resp = req.head(url, timeout=5, allow_redirects=True)
                if resp.status_code < 400:
                    best_url = url
                    break
            except:
                continue
        
        output.append("")
        output.append(f"[URL] Opening in browser: {best_url}")
        try:
            webbrowser.open(best_url, new=2)
        except:
            output.append("  (Could not open browser automatically)")

    # Write to shared memory
    if md_files:
        remember(
            command="/browse",
            query=location_str,
            result_summary=f"Found {len(md_files)} files for {location_str}",
            source_type="chronicle",
            confidence=0.95,
        )

    return "\n".join(output)