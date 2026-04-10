"""Fetch and analyze URL content with caching, rate limiting, and content extraction"""

import requests
import socket
from urllib.parse import urlparse
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.cache import get_cache
from core.rate_limiter import get_rate_limiter, get_robots_parser
from core.pacer import get_pacer
from utils.content_parser import get_extractor

def fetch_command(args=None):
    if not args:
        print("Usage: /fetch [url]")
        print("Example: /fetch https://www.uscourts.gov")
        return

    url = args.strip()
    print(f"\n🌐 Fetching: {url}\n")

    # Validate URL format
    try:
        parsed = urlparse(url)
        if not parsed.scheme:
            url = "https://" + url
            print(f"  Added https:// → {url}")
    except Exception as e:
        print(f"❌ Invalid URL format: {e}")
        return

    # Check cache first
    cache = get_cache()
    cached = cache.get(url, max_age_hours=24)
    if cached:
        print(f"  📦 Cache HIT (fetched {cached['hit_count']} times, expires in {((cached['expires_at'] - __import__('time').time()) / 3600):.1f} hours)")
        content = cached["content"]
        print("\n" + "="*60)
        print("📄 CACHED CONTENT PREVIEW")
        print("="*60)
        print(f"Status: CACHED ✅")
        print(f"Content-Type: {cached['content_type']}")
        print(f"Size: {cached['size']} characters")
        print(f"Fetched at: {__import__('datetime').datetime.fromtimestamp(cached['fetched_at']).strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n--- Extracted Content (First 1500 characters) ---")
        
        # Use content extractor
        extractor = get_extractor()
        clean_text = extractor.strip_html(content, max_length=1500)
        print(clean_text)
        
        # Extract legal citations if it's a legal site
        if extractor.is_legal_site(url):
            citations = extractor.extract_legal_citations(clean_text)
            if citations:
                print(f"\n📖 Legal Citations Found: {', '.join(citations[:5])}")
        
        print("="*60)
        return

    # Check robots.txt
    robots = get_robots_parser()
    if not robots.is_allowed(url):
        print(f"  🤖 robots.txt disallows crawling this URL")
        print("  Skipping...")
        return
    
    # Get crawl delay
    crawl_delay = robots.get_crawl_delay(url)
    print(f"  ⏱️  Crawl delay: {crawl_delay} seconds")
    
    # Rate limiting
    rate_limiter = get_rate_limiter()
    rate_limiter.wait_if_needed(url)
    
    # Resolve domain
    domain = urlparse(url).netloc
    print(f"  Resolving domain: {domain}")
    try:
        socket.gethostbyname(domain)
        print(f"  ✅ Domain resolved")
    except socket.gaierror:
        print(f"  ❌ Cannot resolve domain: {domain}")
        return

    # Check if it's a PACER URL
    pacer = get_pacer()
    is_pacer = pacer.is_pacer_url(url)
    if is_pacer:
        print(f"  ⚖️  PACER URL detected")

    # Try multiple user agents
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    ]

    for i, ua in enumerate(user_agents[:2]):
        try:
            print(f"\n  Attempt {i+1}...")
            response = requests.get(
                url, 
                timeout=30, 
                headers={
                    'User-Agent': ua,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Connection': 'keep-alive',
                },
                allow_redirects=True
            )
            response.raise_for_status()

            content = response.text
            
            # Cache the content
            cache.set(url, content, response.headers.get('content-type', 'text/html'), ttl_hours=24)
            print(f"  💾 Cached for 24 hours")
            
            # Extract clean text
            extractor = get_extractor()
            clean_text = extractor.strip_html(content, max_length=2000)
            
            print("\n" + "="*60)
            print("📄 CONTENT PREVIEW")
            print("="*60)
            print(f"Status: {response.status_code} ✅")
            print(f"Content-Type: {response.headers.get('content-type', 'unknown')}")
            print(f"Size: {len(content)} characters")
            print(f"Final URL: {response.url}")
            
            # Show extracted content
            print("\n--- Extracted Content ---")
            print(clean_text)
            
            # Extract links for legal sites
            if extractor.is_legal_site(url):
                links = extractor.extract_links(content, url)
                if links:
                    print(f"\n🔗 Related Links ({len(links)}):")
                    for link in links[:5]:
                        print(f"  • {link[:80]}...")
                
                # Extract legal citations
                citations = extractor.extract_legal_citations(clean_text)
                if citations:
                    print(f"\n📖 Legal Citations Found: {', '.join(citations[:5])}")
            
            # PACER-specific extraction
            if is_pacer:
                case_number = pacer.extract_case_number(content)
                if case_number:
                    print(f"\n⚖️ Case Number: {case_number}")
                    print(f"   Docket URL: {pacer.format_pacer_docket(case_number)}")
                
                judge = pacer.extract_judge_name(content)
                if judge:
                    print(f"👨‍⚖️ Judge: {judge}")
                
                filing_date = pacer.extract_filing_date(content)
                if filing_date:
                    print(f"📅 Filing Date: {filing_date}")
            
            print("="*60)
            return

        except requests.exceptions.SSLError as e:
            print(f"  ❌ SSL Error: {e}")
            continue
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Error: {e}")
            continue

    print(f"\n❌ Failed to fetch after {len(user_agents)} attempts")
    print("\n💡 Suggestions:")
    print("  1. Try a different URL")
    print("  2. The website may be blocking automated requests")
    print("  3. Use /llm to ask about the content instead")

# Command registration
name = "/fetch"
run = fetch_command
