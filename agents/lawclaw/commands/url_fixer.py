# agents/lawclaw/commands/url_fixer.py - Intelligent URL correction
# When a URL 404s, tries common fixes to find the working version.
import re
import requests

def fix_url(url, timeout=5):
    """Try to fix a broken URL. Returns (fixed_url, was_fixed)."""
    if not url or not url.startswith('http'):
        return url, False
    
    # First check if it works
    try:
        r = requests.head(url, timeout=timeout, allow_redirects=True)
        if r.status_code == 200:
            return url, False
    except:
        pass
    
    original = url
    
    # Fix 1: Try HTTPS if HTTP
    if url.startswith('http://'):
        try:
            https_url = url.replace('http://', 'https://', 1)
            r = requests.head(https_url, timeout=timeout, allow_redirects=True)
            if r.status_code == 200:
                return https_url, True
        except:
            pass
    
    # Fix 2: Remove trailing slash
    if url.endswith('/'):
        try:
            no_slash = url.rstrip('/')
            r = requests.head(no_slash, timeout=timeout, allow_redirects=True)
            if r.status_code == 200:
                return no_slash, True
        except:
            pass
    
    # Fix 3: Add www if missing
    if '://' in url and 'www.' not in url:
        try:
            parts = url.split('://')
            www_url = f"{parts[0]}://www.{parts[1]}"
            r = requests.head(www_url, timeout=timeout, allow_redirects=True)
            if r.status_code == 200:
                return www_url, True
        except:
            pass
    
    # Fix 4: Remove www if present
    if 'www.' in url:
        try:
            no_www = url.replace('www.', '', 1)
            r = requests.head(no_www, timeout=timeout, allow_redirects=True)
            if r.status_code == 200:
                return no_www, True
        except:
            pass
    
    # Fix 5: Try the root domain
    try:
        domain = url.split('://')[1].split('/')[0]
        root = f"{url.split('://')[0]}://{domain}"
        r = requests.head(root, timeout=timeout, allow_redirects=True)
        if r.status_code == 200:
            return root, True
    except:
        pass
    
    return original, False

def validate_urls(urls, timeout=5):
    """Validate a list of URLs, fixing broken ones. Returns (working, broken, fixed)."""
    working = []
    broken = []
    fixed = []
    
    for url in urls:
        if not url or not url.startswith('http'):
            broken.append((url, 'invalid format'))
            continue
        
        fixed_url, was_fixed = fix_url(url, timeout)
        
        if was_fixed:
            fixed.append((url, fixed_url))
            working.append(fixed_url)
        elif fixed_url == url:
            working.append(url)
        else:
            broken.append((url, 'could not fix'))
    
    return working, broken, fixed

print('url_fixer.py loaded')
