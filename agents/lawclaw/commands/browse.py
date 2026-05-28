"""browse command - Display jurisdiction files in CLI + open URLs in browser"""
import webbrowser
import re
from pathlib import Path

name = "/browse"

from agents.lawclaw.commands._memory import show_prior, remember


def _safe_browse_path(s: str, max_len: int = 100) -> str:
    """Sanitize browse path input — CodeQL path injection compliance."""
    s = str(s).replace('..', '').replace('\\', '').replace('/', ' ')
    return re.sub(r'[^a-zA-Z0-9\s\-\']', '', s.strip())[:max_len]


def run(args):
    if not args:
        return "[BROWSE] Usage: /browse [state] [county] [city] -- e.g., /browse MA, /browse MA Worcester, /browse MA Worcester Worcester"

    parts = args.strip().split()
    raw_state = parts[0].upper() if len(parts) > 0 else ""
    raw_county = parts[1] if len(parts) > 1 else ""
    raw_city = parts[2] if len(parts) > 2 else ""

    # Sanitize all components into visibly safe variables — CodeQL requires this
    safe_state = _safe_browse_path(raw_state, 2)
    if len(safe_state) != 2 or not safe_state.isalpha():
        return f"[ERROR] Invalid state code: {raw_state}. Use 2-letter code like MA, TX, CA."
    
    safe_county = _safe_browse_path(raw_county, 80) if raw_county else ""
    safe_city = _safe_browse_path(raw_city, 80) if raw_city else ""

    output = []
    location_parts = [p for p in [safe_city, safe_county, safe_state] if p]
    location_str = ", ".join(location_parts)
    
    output.append("")
    output.append(f"BROWSE: {location_str}")
    output.append("=" * 60)

    prior = show_prior(args, output)

    LAW_REFS = Path(__file__).parent.parent.parent.parent / "agents" / "webclaw" / "references" / "lawclaw"
    juris_root = (LAW_REFS / "jurisdictions" / "us").resolve()
    base = (juris_root / safe_state).resolve()
    
    # Verify path stays within jurisdiction root
    try:
        base.relative_to(juris_root)
    except ValueError:
        output.append("")
        output.append(f"[ERROR] Invalid path for {location_str}")
        return "\n".join(output)
    
    if safe_county:
        base = (base / safe_county).resolve()
        try:
            base.relative_to(juris_root)
        except ValueError:
            output.append("")
            output.append(f"[ERROR] Invalid path for {location_str}")
            return "\n".join(output)
    if safe_city:
        base = (base / safe_city).resolve()
        try:
            base.relative_to(juris_root)
        except ValueError:
            output.append("")
            output.append(f"[ERROR] Invalid path for {location_str}")
            return "\n".join(output)

    if not base.exists():
        output.append("")
        output.append(f"[EMPTY] No jurisdiction data found for {location_str}")
        output.append("[TIP] Try /list to see available states")
        output.append("[TIP] Try /search [query] to search all references")
        return "\n".join(output)

    md_files = list(base.glob("*.md"))
    if not safe_city and safe_county:
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
            if safe_state.lower() in url_lower:
                score += 50
            if safe_county and safe_county.lower() in url_lower:
                score += 75
            if safe_city and safe_city.lower() in url_lower:
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