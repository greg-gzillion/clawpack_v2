"""search command - Search local legal references"""
from pathlib import Path

name = "/search"

def run(args):
    if not args:
        return "?? Usage: /search [case name, citation, or keyword]"
    
    LEGAL_REFS = Path("C:/Users/greg/dev/clawpack_v2/agents/webclaw/references/lawclaw")
    
    output = []
    output.append(f"\n?? SEARCHING: {args}")
    output.append("-"*70)
    
    results = []
    if LEGAL_REFS.exists():
        for area in LEGAL_REFS.iterdir():
            if area.is_dir():
                for md_file in area.rglob("*.md"):
                    try:
                        content = md_file.read_text(encoding='utf-8', errors='ignore')
                        if args.lower() in content.lower():
                            results.append(md_file)
                            if len(results) >= 5:
                                break
                    except:
                        pass
            if len(results) >= 5:
                break
    
    if results:
        output.append(f"\n? Found {len(results)} results:\n")
        for r in results:
            rel_path = r.relative_to(LEGAL_REFS)
            area = rel_path.parts[0] if len(rel_path.parts) > 0 else "unknown"
            output.append(f"\n{'='*70}")
            output.append(f"?? {area.upper()}")
            output.append(f"?? {r.name}")
            output.append('='*70)
            content = r.read_text(encoding='utf-8', errors='ignore')
            output.append(content)
            if len(content) > 1500:
                output.append("\n... (truncated)")
    else:
        output.append("\n? No results found")
        output.append("\n?? Try /list to see available topics or /llm for AI research")
    
    return "\n".join(output)
