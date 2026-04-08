"""search command - Search case law and fetch from URLs"""

name = "/search"

def run(args):
    if not args:
        print("Usage: /search TERM")
        print("Example: /search bankruptcy")
        return
    
    query = args.lower().strip()
    from pathlib import Path
    import requests
    import re
    
    webclaw_path = Path(__file__).parent.parent.parent / "webclaw" / "references" / "lawclaw"
    
    if not webclaw_path.exists():
        print(f"❌ Reference data not found at: {webclaw_path}")
        return
    
    print(f"\n🔍 Searching for '{query}'...\n")
    
    # Find all .md files that contain the query term
    results = []
    for md_file in webclaw_path.rglob("*.md"):
        try:
            content = md_file.read_text(encoding='utf-8', errors='ignore')
            if query in content.lower():
                # Extract URLs from the .md file
                urls = re.findall(r'https?://[^\s\)\]>]+', content)
                if urls:
                    results.append({
                        "file": md_file.relative_to(webclaw_path),
                        "urls": urls[:3]  # First 3 URLs
                    })
                if len(results) >= 5:
                    break
        except:
            pass
    
    if not results:
        print("❌ No results found")
        return
    
    print(f"✅ Found {len(results)} results:\n")
    
    for result in results:
        print(f"📄 {result['file']}")
        for url in result['urls']:
            print(f"   🔗 {url}")
            # Fetch the URL content (via WebClaw or directly)
            try:
                print(f"   📡 Fetching content...")
                response = requests.get(url, timeout=10, headers={'User-Agent': 'LawClaw/1.0'})
                if response.status_code == 200:
                    # Extract text from HTML
                    text = re.sub(r'<[^>]+>', ' ', response.text)
                    text = re.sub(r'\s+', ' ', text)
                    # Show first 500 characters
                    preview = text[:500].strip()
                    print(f"   📖 {preview}...")
                else:
                    print(f"   ❌ Failed to fetch (status {response.status_code})")
            except Exception as e:
                print(f"   ❌ Error fetching: {e}")
            print()
        print("-" * 50)
